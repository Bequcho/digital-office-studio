<?php
defined('ABSPATH')||exit;
global $product;
if(!$product || !$product->is_visible())return;
forme_card($product);
