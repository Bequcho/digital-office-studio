<?php
if (!defined('ABSPATH')) exit;
add_action('after_setup_theme',function(){
  add_theme_support('title-tag');
  add_theme_support('post-thumbnails');
  add_theme_support('woocommerce');
  add_theme_support('html5',['search-form','gallery','caption']);
  register_nav_menus(['primary'=>'Меню магазина']);
});
add_action('wp_enqueue_scripts', function(){
 wp_enqueue_style('forme', get_stylesheet_uri(),[], '1.0.0');
});
function forme_shop(){return function_exists('wc_get_page_permalink') ? wc_get_page_permalink('shop') : home_url('/');}
function forme_cart(){return function_exists('wc_get_cart_url') ? wc_get_cart_url() : home_url('/');}
function forme_img_url($product){$url=$product->get_meta('_forme_image');return $url?:'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8c?w=900&q=85';}
function forme_card($product){
 if(!$product || !$product->is_visible())return;
 $url=esc_url($product->get_permalink()); $img=esc_url(forme_img_url($product));
 echo '<article class="product-card"><a class="product-img" href="'.$url.'"><img src="'.$img.'" alt="'.esc_attr($product->get_name()).'" loading="lazy">';
 if($product->is_on_sale()) echo '<span class="product-badge">ОСОБАЯ ЦЕНА</span>';
 echo '</a><div class="product-info"><div><a href="'.$url.'"><strong>'.esc_html($product->get_name()).'</strong></a><div class="small">'.esc_html(wc_get_product_category_list($product->get_id(),', ','','')).'</div></div><span class="price">'.$product->get_price_html().'</span></div>';
 echo '<a class="quick-add" href="'.esc_url($product->add_to_cart_url()).'">+ В корзину</a></article>';
}
add_filter('woocommerce_email_enabled_new_order','__return_false');
add_filter('woocommerce_email_enabled_customer_processing_order','__return_false');
add_filter('woocommerce_email_enabled_customer_on_hold_order','__return_false');
add_filter('woocommerce_email_enabled_customer_completed_order','__return_false');
add_filter('woocommerce_order_button_text',function(){return 'Оформить тестовый заказ';});
add_action('woocommerce_before_checkout_form',function(){echo '<div class="demo-ribbon"><strong>Демо-режим:</strong> все товары и заказы вымышленные. Оплата не производится, реальные данные не вводите.</div>';},5);
add_filter('woocommerce_checkout_fields',function($fields){
 foreach(['billing_company','billing_address_2','billing_state','billing_postcode'] as $key) unset($fields['billing'][$key]);
 return $fields;
});
