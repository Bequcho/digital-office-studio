<?php
defined('ABSPATH')||exit;
global $product;
if(!$product)return;
?>
<div class="single-grid">
<div class="single-photo"><img src="<?php echo esc_url(forme_img_url($product)); ?>" alt="<?php echo esc_attr($product->get_name()); ?>"></div>
<div class="single-summary"><span class="eyebrow">FORME HOME · КОЛЛЕКЦИЯ</span><h1><?php echo esc_html($product->get_name()); ?></h1>
<div class="price"><?php echo $product->get_price_html(); ?></div>
<div class="woocommerce-product-details__short-description"><?php echo wpautop(wp_kses_post($product->get_short_description())); ?></div>
<?php woocommerce_template_single_add_to_cart(); ?>
<div class="single-features"><div>✓ Продукт представлен в ознакомительных целях</div><div>✓ Тестовая корзина без оплаты</div><div>✓ WordPress + WooCommerce</div></div>
<div class="product_meta">Артикул: <?php echo esc_html($product->get_sku()); ?></div>
</div></div>
<section style="margin-bottom:90px"><div class="section-head"><div><span class="eyebrow">ВАМ ТАКЖЕ ПОНРАВИТСЯ</span><h2>Вдохновение рядом.</h2></div></div><div class="product-grid"><?php
$related=wc_get_related_products($product->get_id(),4);
foreach($related as $id){$p=wc_get_product($id); if($p)forme_card($p);}
?></div></section>