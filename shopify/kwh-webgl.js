/* Self-contained WebGL2 glTF bottle renderer. No network libraries required. */
(() => {
  'use strict';

  const VERTEX = `#version 300 es
    in vec3 aPosition;
    in vec3 aNormal;
    in vec2 aUV;
    uniform mat4 uProjection;
    uniform float uAngle;
    uniform float uDistance;
    out vec3 vNormal;
    out vec2 vUV;
    out vec3 vPosition;
    void main(){
      float c=cos(uAngle), s=sin(uAngle);
      vec3 p=vec3(c*aPosition.x+s*aPosition.z,
                  aPosition.y-.154,
                  -s*aPosition.x+c*aPosition.z);
      vec3 n=vec3(c*aNormal.x+s*aNormal.z, aNormal.y,
                  -s*aNormal.x+c*aNormal.z);
      float ct=cos(-.095), st=sin(-.095);
      p=vec3(p.x,ct*p.y-st*p.z,st*p.y+ct*p.z);
      n=vec3(n.x,ct*n.y-st*n.z,st*n.y+ct*n.z);
      p.z-=uDistance;
      vPosition=p;
      vNormal=n;
      vUV=aUV;
      gl_Position=uProjection*vec4(p,1.0);
    }`;
  const FRAGMENT = `#version 300 es
    precision highp float;
    in vec3 vNormal;
    in vec2 vUV;
    in vec3 vPosition;
    uniform vec3 uColor;
    uniform sampler2D uTexture;
    uniform bool uTextured;
    uniform float uGloss;
    out vec4 fragColor;
    void main(){
      vec3 n=normalize(vNormal);
      // Two softboxes in a neutral photo studio; broad reflection sources
      // complement the photographic highlights without painting over the art.
      vec3 light=normalize(vec3(-.62,.66,.76));
      vec3 fill=normalize(vec3(.78,.22,.48));
      vec3 viewDir=normalize(-vPosition);
      float diffuse=max(dot(n,light),0.0);
      float fillLight=max(dot(n,fill),0.0);
      float facing=clamp(dot(n,viewDir),0.0,1.0);
      float fresnel=pow(1.0-facing,4.0);
      vec3 base=uTextured?texture(uTexture,vUV).rgb:uColor;
      if(uTextured){
        // PBR-inspired material separation: paper absorbs light diffusely,
        // coloured glass catches long vertical softbox reflections, and the
        // metallized capsule gets a smaller satiny highlight. Both paper
        // zones are different sizes: front near U=.5, reverse near U=0/1.
        float fromFront=abs(vUV.x-.5);
        float frontPaper=(1.0-smoothstep(.15,.20,fromFront))
          *smoothstep(.405,.445,vUV.y)
          *(1.0-smoothstep(.865,.91,vUV.y));
        float rearPaper=smoothstep(.31,.365,fromFront)
          *smoothstep(.445,.495,vUV.y)
          *(1.0-smoothstep(.792,.85,vUV.y));
        float paper=clamp(max(frontPaper,rearPaper),0.0,1.0);
        float capsule=1.0-smoothstep(.185,.23,vUV.y);
        float glass=(1.0-paper)*(1.0-capsule);
        float studioLight=mix(.79+.19*diffuse+.08*fillLight,
          .995+.005*diffuse,smoothstep(.24,.83,facing));
        float ribbonA=exp(-pow((n.x+.68)/.19,2.0))*max(n.z+.26,0.0);
        float ribbonB=exp(-pow((n.x-.79)/.12,2.0))*max(n.z+.31,0.0);
        float reflected=(ribbonA*.125+ribbonB*.082+fresnel*.12)*glass;
        float satin=exp(-pow((n.x+.42)/.24,2.0))*.09*capsule;
        vec3 glassColor=base*studioLight+vec3(.95,.91,.85)*reflected;
        vec3 paperColor=base*(.985+.015*diffuse);
        vec3 capColor=base*(.965+.035*diffuse)+vec3(.96,.82,.58)*satin;
        vec3 color=mix(glassColor,paperColor,paper);
        color=mix(color,capColor,capsule);
        fragColor=vec4(clamp(color,0.0,1.0),1.0);
      }else{
        float lit=.44+.57*diffuse+.23*fillLight;
        float streak=pow(max(dot(n,normalize(vec3(-.4,.02,.92))),0.0),22.0);
        float spec=pow(max(dot(reflect(-light,n),viewDir),0.0),70.0);
        vec3 color=base*lit + vec3(.74,.77,.79)*(streak*.38 + spec*.42)*uGloss;
        color+=vec3(.14,.12,.10)*fresnel*uGloss;
        fragColor=vec4(clamp(color,0.0,1.0),1.0);
      }
    }`;

  function shader(gl, type, code) {
    const value=gl.createShader(type);
    gl.shaderSource(value,code);
    gl.compileShader(value);
    if(!gl.getShaderParameter(value,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(value));
    return value;
  }

  function program(gl){
    const p=gl.createProgram();
    gl.attachShader(p,shader(gl,gl.VERTEX_SHADER,VERTEX));
    gl.attachShader(p,shader(gl,gl.FRAGMENT_SHADER,FRAGMENT));
    gl.linkProgram(p);
    if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(p));
    return p;
  }

  function projection(aspect){
    const near=.01, far=10, f=1/Math.tan(31*Math.PI/360);
    return new Float32Array([
      f/aspect,0,0,0,
      0,f,0,0,
      0,0,-(far+near)/(far-near),-1,
      0,0,-2*far*near/(far-near),0,
    ]);
  }

  function parseGLB(source){
    const data=new DataView(source);
    if(data.getUint32(0,true)!==0x46546c67||data.getUint32(4,true)!==2)
      throw new Error('Invalid glTF model');
    const jsonLength=data.getUint32(12,true);
    const json=JSON.parse(new TextDecoder().decode(new Uint8Array(source,20,jsonLength)));
    const binaryStart=20+jsonLength+8;
    const views=json.bufferViews;
    const chunk=index=>{
      const v=views[index];
      return new Uint8Array(source,binaryStart+(v.byteOffset||0),v.byteLength);
    };
    const accessor=index=>{
      const a=json.accessors[index];
      const view=views[a.bufferView];
      const bytes=binaryStart+(view.byteOffset||0)+(a.byteOffset||0);
      const component=a.componentType===5126?Float32Array:a.componentType===5123?Uint16Array:Uint32Array;
      const size={SCALAR:1,VEC2:2,VEC3:3,VEC4:4}[a.type];
      return new component(source.slice(bytes,bytes+a.count*size*component.BYTES_PER_ELEMENT));
    };
    return {json,chunk,accessor};
  }

  function buffer(gl,data,target){
    const result=gl.createBuffer();
    gl.bindBuffer(target,result);
    gl.bufferData(target,data,gl.STATIC_DRAW);
    return result;
  }

  async function loadTexture(gl, bytes, mime){
    const bitmap=await createImageBitmap(new Blob([bytes],{type:mime}),{premultiplyAlpha:'none'});
    const texture=gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D,texture);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,bitmap);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
    gl.generateMipmap(gl.TEXTURE_2D);
    bitmap.close?.();
    return texture;
  }

  async function prepare(gl,p,source){
    const {json,chunk,accessor}=parseGLB(source);
    const textures=await Promise.all(json.images.map(img=>loadTexture(gl,chunk(img.bufferView),img.mimeType)));
    const meshes=[];
    const attributes={position:gl.getAttribLocation(p,'aPosition'),normal:gl.getAttribLocation(p,'aNormal'),uv:gl.getAttribLocation(p,'aUV')};
    for(const mesh of json.meshes){
      for(const primitive of mesh.primitives){
        const vao=gl.createVertexArray();
        gl.bindVertexArray(vao);
        for(const [semantic,location,components] of [
          ['POSITION',attributes.position,3],['NORMAL',attributes.normal,3],['TEXCOORD_0',attributes.uv,2]
        ]){
          const contents=accessor(primitive.attributes[semantic]);
          buffer(gl,contents,gl.ARRAY_BUFFER);
          gl.enableVertexAttribArray(location);
          gl.vertexAttribPointer(location,components,gl.FLOAT,false,0,0);
        }
        const indices=accessor(primitive.indices);
        buffer(gl,indices,gl.ELEMENT_ARRAY_BUFFER);
        gl.bindVertexArray(null);
        const material=json.materials[primitive.material].pbrMetallicRoughness;
        const imageId=material.baseColorTexture?.index;
        meshes.push({vao,count:indices.length,type:indices instanceof Uint16Array?gl.UNSIGNED_SHORT:gl.UNSIGNED_INT,
          color:material.baseColorFactor.slice(0,3),texture:imageId===undefined?null:textures[imageId],
          gloss:material.metallicFactor>.3?1.15:.78});
      }
    }
    return meshes;
  }

  async function create(canvas,url){
    const gl=canvas.getContext('webgl2',{alpha:true,antialias:true,depth:true,premultipliedAlpha:false});
    if(!gl)throw new Error('WebGL2 not available');
    const p=program(gl);
    const response=await fetch(url);
    if(!response.ok)throw new Error('Cannot load bottle model: '+response.status);
    const meshes=await prepare(gl,p,await response.arrayBuffer());
    gl.useProgram(p);
    gl.uniform1i(gl.getUniformLocation(p,'uTexture'),0);
    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.CULL_FACE);
    gl.cullFace(gl.BACK);
    const uniforms={
      projection:gl.getUniformLocation(p,'uProjection'),angle:gl.getUniformLocation(p,'uAngle'),
      distance:gl.getUniformLocation(p,'uDistance'),color:gl.getUniformLocation(p,'uColor'),
      textured:gl.getUniformLocation(p,'uTextured'),gloss:gl.getUniformLocation(p,'uGloss'),
    };
    return {render(degrees,zoomed){
      const bounds=canvas.getBoundingClientRect();
      const density=Math.min(devicePixelRatio||1,2);
      const w=Math.max(1,Math.round(bounds.width*density));
      const h=Math.max(1,Math.round(bounds.height*density));
      if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h}
      gl.viewport(0,0,w,h);
      gl.clearColor(0,0,0,0);
      gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
      gl.useProgram(p);
      gl.uniformMatrix4fv(uniforms.projection,false,projection(w/h));
      gl.uniform1f(uniforms.angle,degrees*Math.PI/180);
      gl.uniform1f(uniforms.distance,zoomed?.57:.70);
      for(const mesh of meshes){
        gl.bindVertexArray(mesh.vao);
        gl.uniform3fv(uniforms.color,mesh.color);
        gl.uniform1i(uniforms.textured,!!mesh.texture);
        gl.uniform1f(uniforms.gloss,mesh.gloss);
        if(mesh.texture){gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,mesh.texture)}
        gl.drawElements(gl.TRIANGLES,mesh.count,mesh.type,0);
      }
      gl.bindVertexArray(null);
    }};
  }

  window.Kakheti3DViewer={create};
})();

