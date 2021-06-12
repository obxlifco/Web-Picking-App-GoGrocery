
export var banner = `
<div class="top_banner">
	<a href="javascript:void(0)">
    	<img alt="{{banner_alt}}" src="{{banner_url}}">
    </a>
</div>`;
export var carousel = `<div class="slideshow-container">
  <div class="mySlides fade">
    <div class="numbertext">1 / 3</div>
    <img src="img1.jpg" style="width:100%">
    <div class="text">Caption Text</div>
  </div>

  <div class="mySlides fade">
    <div class="numbertext">2 / 3</div>
    <img src="img2.jpg" style="width:100%">
    <div class="text">Caption Two</div>
  </div>

  <div class="mySlides fade">
    <div class="numbertext">3 / 3</div>
    <img src="img3.jpg" style="width:100%">
    <div class="text">Caption Three</div>
  </div>
  <a class="prev" (click)="plusSlides(-1)">&#10094;</a>
  <a class="next" (click)="plusSlides(1)">&#10095;</a>
</div>
<br>
<div style="text-align:center">
  <span class="dot" (click)="currentSlide(1)"></span> 
  <span class="dot" (click)="currentSlide(2)"></span> 
  <span class="dot" (click)="currentSlide(3)"></span> 
</div>`;

export var info_box = `
<section class="temp_feature">
    <div class="container">
        <div class="row">
            <div class="col-md-6 col-lg-3">
                <div class="fech_box">
                    <i class="fa {{icon1}}"></i>
                    <h5>{{heading1}}</h5>
                    <p>{{desc1}}</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="fech_box">
                    <i class="fa {{icon2}}"></i>
                    <h5>{{heading2}}</h5>
                    <p>{{desc2}}</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="fech_box">
                    <i class="fa {{icon3}}"></i>
                    <h5>{{heading3}}</h5>
                    <p>{{desc3}}</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="fech_box">
                    <i class="fa {{icon4}}"></i>
                    <h5>{{heading4}}</h5>
                    <p>{{desc4}}</p>
                </div>
            </div>
        </div>
    </div>
</section>`;
export var featured_box_v = `
<section>
	<div class="container">
	    <div class="row">
	        <div class="col-sm-4">
	            <a href="javascript:void(0)">
		            <div class="catagory">
			            <img src="{{box1_img}}" alt="">
			            <div class="title">{{box1_text}}</div>
		            </div>
	            </a>
	        </div>
	        <div class="col-sm-4">
	        	<a href="javascript:void(0)">
		            <div class="catagory">
			            <img src="{{box2_img}}" alt="">
			            <div class="title">{{box2_text}}</div>
		            </div>
	            </a>
	        </div>
	        <div class="col-sm-4">
	        	<a href="javascript:void(0)">
		            <div class="catagory">
			            <img src="{{box3_img}}" alt="">
			            <div class="title">{{box3_text}}</div>
		            </div>
	            </a>
	        </div>
	    </div>
	</div>    
</section>

`;
export var featured_box_h = `

<section>
	<div class="container">
	    <div class="row">
	        <div class="col-sm-6">
	            <div class="catagory1">
	                <div class="img-part"><img src="{{box1_img}}"></div>
	                <div class="text-part">
	                    <div class="row align-items-center">
	                        <div class="col">
	                            <h4>{{box1_heading}}</h4>
	                            <p>{{box1_desc}}</p>
	                        </div>                                
	                        <div class="col-auto ml-auto">
	                            <a href="javascript:void(0)">
		                            <button class="btn-main mat-raised-button" mat-raised-button>
			                            <span class="mat-button-wrapper">{{box1_btn}}</span>
			                            <div class="mat-button-ripple mat-ripple"></div>
			                            <div class="mat-button-focus-overlay"></div>
		                            </button>
	                            </a>
	                        </div>
	                    </div>
	                </div>
	            </div>
	        </div>
	        <div class="col-sm-6">
	            <div class="catagory1">
	                <div class="img-part"><img src="{{box2_img}}"></div>
	                <div class="text-part">
	                    <div class="row align-items-center">
	                        <div class="col">
	                            <h4>{{box2_heading}}</h4>
	                            <p>{{box2_desc}}</p>
	                        </div>                                
	                        <div class="col-auto ml-auto">
	                        	<a href="javascript:void(0)">
		                            <button class="btn-main mat-raised-button" mat-raised-button>
		                            	<span class="mat-button-wrapper">{{box2_btn}}</span>
		                            	<div class="mat-button-ripple mat-ripple"></div>
		                            	<div class="mat-button-focus-overlay"></div>
		                            </button>
	                            </a>
	                        </div>
	                    </div>
	                </div>
	            </div>
	        </div>
	    </div>
	</div>    
</section>

`;
export var OurFeature = '';
export var category_banner = '';
export var promotion_banner = '';
export var product_list = `<section class="container-fluid">
          <div class="row">
              <div class="col-12">
                  <div class="container_cuswrap">
                      <div class="shop_category">
                          <div class="innerheader">
                              <h3>Shop By Category</h3>
                                  
                              <div class="showall_text"><a href="#">Show All Category<span class="icon-back"></span></a></div>
                          </div>
                          <div class="categoryrow">
                              <div class="categorybox">
                                  <div class="image_sec cata_color_a"><span class="icon-apple-black-silhouette-with-a-leaf"></span></div>
                                  <div class="text_sec">text</div>
                              </div>
                              <div class="categorybox">
                                  <div class="image_sec cata_color_b"><span class="icon-pumpkin-vegetable"></span></div>
                                  <div class="text_sec">Vegetables</div>
                              </div>
                              <div class="categorybox">
                                  <div class="image_sec cata_color_c"><span class="icon-cupcake-dessert"></span></div>
                                  <div class="text_sec">Bakery</div>
                              </div>
                              <div class="categorybox">
                                  <div class="image_sec cata_color_d"><span class="icon-coffee-beans"></span></div>
                                  <div class="text_sec">Coffee & Tea</div>
                              </div>
                              <div class="categorybox">
                                  <div class="image_sec cata_color_e"><span class="icon-fish"></span></div>
                                  <div class="text_sec">Fish & Meat</div>
                              </div>
                              <div class="categorybox">
                                  <div class="image_sec cata_color_f"><span class="icon-perfume-bottle"></span></div>
                                  <div class="text_sec">Personal Care</div>
                              </div>
                              <div class="categorybox">
                                  <div class="image_sec cata_color_g"><span class="icon-drink"></span></div>
                                  <div class="text_sec">Beverages</div>
                              </div>
                              <div class="categorybox">
                                  <div class="image_sec cata_color_h"><span class="icon-cereals"></span></div>
                                  <div class="text_sec">Organic</div>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </section>`;
export var sell_or_deal_prduct = `<section class="container-fluid" *ngIf="isCMS">
          <div class="row">
              <div class="col-12">
                  <div class="container_cuswrap">
                          <div class="innerheader">
                                  <h3>{{heading_text}}</h3>  
                                  <div class="showall_text"><a href="#">Show All Category<span class="icon-back"></span></a></div>
                              </div>
                      <div class="product_row">
                          <div class="productblog">
                              <div class="likecard">
                                  <a href="#">
                                      <span class="icon-wishlist-2"></span>    
                                      <span class="icon-wishlist"></span>
                                  </a>
                              </div>
                              <div class="imagebox">
                                   <img src="assets/images/Layer_16.png">
                              </div>
                              <div class="textbox">
                                      <div class="vag_simbol"></div>
                                      <div class="textrow">
                                         <p><span>Fresho</span>Fresh Tomatoes</p>
                                      </div>
                                      <div class="textrow selectrow">
                                           <select placeholder="ssss">
                                               <option>Demo text 1</option>
                                               <option>Demo text 2</option>
                                               <option>Demo text 3</option>
                                               <option>Demo text 4</option>
                                           </select>  
                                      </div>
                                      <div class="textrow">
                                          <p class="pricerow">$35.00 <span>$50.00</span> <span class="off">(30% OFF)</span></p>  
                                      </div>
                                      <div class="textrow last">
                                          <button class="add_tocard">ADD TO CART<span class="icon-back"></span></button>
                                         
                                          <div class="likebox"><a class="liked" href="#"><span class="icon-valentines-heart"></span></a> </div>
                                      </div>
                              </div>
                          </div>
      
                          <div class="productblog">
                                  <div class="likecard wished">
                                      <a href="#">
                                          <span class="icon-wishlist-2"></span>    
                                          <span class="icon-wishlist"></span>
                                      </a>
                                  </div>
                                  <div class="imagebox">
                                          <img src="assets/images/Layer_16.png">
                                  </div>
                                  <div class="textbox">
                                          <div class="vag_simbol non-veg"></div>
                                          <div class="textrow">
                                             <p><span>Fresho</span>Fresh Tomatoes</p>
                                          </div>
                                          <div class="textrow selectrow">
                                               <select placeholder="ssss">
                                                   <option>Demo text 1</option>
                                                   <option>Demo text 2</option>
                                                   <option>Demo text 3</option>
                                                   <option>Demo text 4</option>
                                               </select>  
                                          </div>
                                          <div class="textrow">
                                              <p class="pricerow">$35.00 <span>$50.00</span> <span class="off">(30% OFF)</span></p>  
                                          </div>
                                          <div class="textrow last">
                                              <div class="count_box">
                                                  <button class="count_btn"><span class="icon-minus"></span></button>
                                                      <div class="count_no">5</div>
                                                  <button class="count_btn"><span class="icon-plus"></span></button>
                                              </div>
                                              <div class="likebox"><a class="liked" href="#"><span class="icon-valentines-heart"></span></a> </div>
                                          </div>
                                  </div>
                          </div>
                          <div class="productblog">
                                      <div class="likecard">
                                          <a href="#">
                                              <span class="icon-wishlist-2"></span>    
                                              <span class="icon-wishlist"></span>
                                          </a>
                                      </div>
                                      <div class="imagebox">
                                              <img src="assets/images/Layer_16.png">
                                      </div>
                                      <div class="textbox">
                                              <div class="textrow">
                                                 <p><span>Fresho</span>Fresh Tomatoes</p>
                                              </div>
                                              <div class="textrow selectrow">
                                                   <select placeholder="ssss">
                                                       <option>Demo text 1</option>
                                                       <option>Demo text 2</option>
                                                       <option>Demo text 3</option>
                                                       <option>Demo text 4</option>
                                                   </select>  
                                              </div>
                                              <div class="textrow">
                                                  <p class="pricerow">$35.00 <span>$50.00</span> <span class="off">(30% OFF)</span></p>  
                                              </div>
                                              <div class="textrow last">
                                                  <div class="count_box">
                                                      <button class="count_btn"><span class="icon-minus"></span></button>
                                                          <div class="count_no">5</div>
                                                      <button class="count_btn"><span class="icon-plus"></span></button>
                                                  </div>
                                                  <div class="likebox"><a class="liked" href="#"><span class="icon-valentines-heart"></span></a> </div>
                                              </div>
                                      </div>
                          </div>
      
                          <div class="productblog">
                                  <div class="likecard wished">
                                      <a href="#">
                                          <span class="icon-wishlist-2"></span>    
                                          <span class="icon-wishlist"></span>
                                      </a>
                                  </div>
                                          <div class="imagebox">
                                                  <img src="assets/images/Layer_16.png">
                                          </div>
                                          <div class="textbox">
                                                  <div class="textrow">
                                                     <p><span>Fresho</span>Fresh Tomatoes</p>
                                                  </div>
                                                  <div class="textrow selectrow">
                                                       <select placeholder="ssss">
                                                           <option>Demo text 1</option>
                                                           <option>Demo text 2</option>
                                                           <option>Demo text 3</option>
                                                           <option>Demo text 4</option>
                                                       </select>  
                                                  </div>
                                                  <div class="textrow">
                                                      <p class="pricerow">$35.00 <span>$50.00</span> <span class="off">(30% OFF)</span></p>  
                                                  </div>
                                                  <div class="textrow last">
                                                      <div class="count_box">
                                                          <button class="count_btn"><span class="icon-minus"></span></button>
                                                              <div class="count_no">5</div>
                                                          <button class="count_btn"><span class="icon-plus"></span></button>
                                                      </div>
                                                      <div class="likebox"><a class="liked" href="#"><span class="icon-valentines-heart"></span></a> </div>
                                                  </div>
                                          </div>
                          </div>
      
                          <div class="productblog">
                                  <div class="likecard">
                                          <a href="#">
                                              <span class="icon-wishlist-2"></span>    
                                              <span class="icon-wishlist"></span>
                                          </a>
                                      </div>
                                          
                                              <div class="imagebox">
                                                      <img src="assets/images/Layer_16.png">
                                              </div>
                                              <div class="textbox">
                                                      <div class="textrow">
                                                         <p><span>Fresho</span>Fresh Tomatoes</p>
                                                      </div>
                                                      <div class="textrow selectrow">
                                                           <select placeholder="ssss">
                                                               <option>Demo text 1</option>
                                                               <option>Demo text 2</option>
                                                               <option>Demo text 3</option>
                                                               <option>Demo text 4</option>
                                                           </select>  
                                                      </div>
                                                      <div class="textrow">
                                                          <p class="pricerow">$35.00 <span>$50.00</span> <span class="off">(30% OFF)</span></p>  
                                                      </div>
                                                      <div class="textrow last">
                                                          <div class="count_box">
                                                              <button class="count_btn"><span class="icon-minus"></span></button>
                                                                  <div class="count_no">5</div>
                                                              <button class="count_btn"><span class="icon-plus"></span></button>
                                                          </div>
                                                          <div class="likebox"><a class="liked" href="#"><span class="icon-valentines-heart"></span></a> </div>
                                                      </div>
                                              </div>
                          </div>
      
                      </div>
                  </div>
              </div>
          </div>
      </section>`;
export var subscribenewsletter = `<section class="subcribe_row">
      <div class="container_cuswrap">
          <div class="subcribe_inner">
              <p>{{heading_text}}</p>
              <div class="subscribebox">
                  <div class="inputbox">
                      <input type="text" placeholder="Enter your email Id">
                  </div>
                  <button class="bubcribebtn">subscribe</button>
                  
              </div>
          </div>
      </div>    
</section>`;
export var single_column_layout_text = `
<section class="0-0 container inserted">
  {{html_text}}
</section>`;

export var two_column_layout_text = `
    <section>
        <div class="container">
            <div class="row">
                <div class="col-12 col-md-6">
                    <h2>{{heading_1}}</h2>
                    <div>
                        {{html_text_1}}
                    </div>
                </div>
                
                <div class="col-12 col-md-6">
                    <h2>{{heading_2}}</h2>
                    <div>
                        {{html_text_2}}
                    </div>
                </div>
            </div>
        </div>
    </section>`;

export var three_column_layout_text = `

    <section>
        <div class="container">
            <div class="row">
                <div class="col-12 col-md-4">
                    <h2>{{heading_1}}</h2>
                    <div>
                        {{html_text_1}}
                    </div>
                </div>
                
                <div class="col-12 col-md-4">
                    <h2>{{heading_2}}</h2>
                    <div>
                        {{html_text_2}}
                    </div>
                </div>

                <div class="col-12 col-md-4">
                    <h2>{{heading_3}}</h2>
                    <div>
                        {{html_text_3}}
                    </div>
                </div>
            </div>
        </div>
    </section>`;

export var image_with_text = `
    <section>
        <div class="container">
            <div class="row">
                <div class="col-12 col-md-auto">
                   <div class="img-box singel">
                       <img src="{{img}}" alt="{{img_alt}}">
                   </div>
                </div>
                <div class="col">
                    <h2>{{heading}}</h2>
                    {{desc_text}}
                </div>
            </div>
        </div>
    </section>`;

export var two_side_banner = `
<section>
    <div class="container">
        <div class="row">
            <div class="col-sm-6">
                <div class="catagory1">
                    <a href="javascript:void(0)">
                        <div class="img-part"><img src="{{box1_img}}" alt="{{box1_alt}}"></div>
                    </a>
                </div>
            </div>
            <div class="col-sm-6">
                <div class="catagory1">
                    <a href="javascript:void(0)">
                        <div class="img-part"><img src="{{box2_img}}" alt="{{box2_alt}}"></div>
                    </a>
                </div>
            </div>
        </div>
    </div>    
</section>`;

export var heading_text = `
<div class="container">
    <h2 class="pro_title">{{heading_text}}</h2>
</div>`;

export var default_form = ``;
/////////// EMAIL TEMPLATE WIDGETS //////////
export var email_banner = `
<table cellpadding="0" cellspacing="0" width="100%" border="0">
    <tr>
        <td>
            <table cellpadding="0" cellspacing="0" width="600" border="0">
                <tr>
                    <td style="padding:5px 0px;">
                        <img alt="{{banner_alt}}" src="{{banner_url}}" width="100%" height="auto">
                    </td>
                </tr>
            </table>    
        </td>
    </tr>
</table>`;

export var email_two_side_banner = `
<table cellpadding="0" cellspacing="0" width="100%" border="0">
    <tr>
        <td>
            <table cellpadding="0" cellspacing="0" width="300" border="0" style="float: left;">
                <tr>
                    <td style="padding:5px 5px 5px 0;">
                        <img src="{{box1_img}}" alt="{{box1_alt}}" width="100%" height="auto" >
                    </td>
                </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="300" border="0" style="float: right;">
                <tr>
                    <td style="padding:5px 0 5px 5px;">
                        <img src="{{box2_img}}" alt="{{box2_alt}}" width="100%" height="auto" >
                    </td>
                </tr>
            </table>    
        </td>
    </tr>
</table>`;

export var email_heading_text = `
<table cellpadding="0" cellspacing="0" width="100%" border="0">
    <tr>
        <td>
            <table cellpadding="0" cellspacing="0" width="600" border="0">
                <tr>
                    <td style="padding:15px 0px;" >
                        <h1 style="text-align: center;">{{heading_text}}</h1>
                    </td>
                </tr>
            </table>    
        </td>
    </tr>
</table>`;

export var email_image_with_text = `
<table cellpadding="0" cellspacing="0" width="100%" border="0">
    <tr>
        <td style="padding: 15px 10px;background:#f7f7f7" valign="middle">
            <table cellpadding="0" cellspacing="0" width="290" border="0" style="float: left;">
                <tr>
                    <td style="padding:5px 5px 5px 0;" align="left" valign="middle">
                        <img src="{{img}}" alt="{{img_alt}}" width="100%" height="auto" >
                    </td>
                </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="290" border="0" style="float: right;">
                <tr>
                    <td style="padding:5px 0 5px 5px;">
                        <h3 style="color: #444">{{heading}}</h3>
                        <p style="font-size: 14px;color: #444">{{desc_text}}</p>
                    </td>
                </tr>
            </table>    
        </td>
    </tr>
</table>`;

export var email_two_side_img_text = `
<table cellpadding="0" cellspacing="0" width="100%" border="0">
    <tr>
        <td>
            <table cellpadding="0" cellspacing="0" width="300" border="0" style="float: left;">
                <tr>
                    <td style="padding:5px 5px 5px 0;">
                        <div style="border: #CCC solid 1px;">
                            <img src="{{box1_img}}" width="100%" height="auto" >
                            <div style="padding:10px 10px 0;">
                                <h4 style="color: #444">{{box1_heading}}</h4>
                                <p style="font-size: 14px;color: #444">{{box1_desc}}</p>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="300" border="0" style="float: right;">
                <tr>
                    <td style="padding:5px 0 5px 5px;">
                        <div style="border: #CCC solid 1px;">
                            <img src="{{box2_img}}" width="100%" height="auto" >
                            <div style="padding:10px 10px 0;">
                                <h4 style="color: #444">{{box2_heading}}</h4>
                                <p style="font-size: 14px;color: #444">{{box2_desc}}</p>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>    
        </td>
    </tr>
</table>`;

export var email_single_col_text = `
<table cellpadding="0" cellspacing="0" width="100%" border="0">
    <tr>
        <td style="padding: 15px 10px;background:#f7f7f7" valign="middle">
            <table cellpadding="0" cellspacing="0" width="100%" border="0" style="float: right;">
                <tr>
                    <td style="padding:5px 0 5px 5px;" class="0-0 container inserted">
                        {{html_text}}
                    </td>
                </tr>
            </table>    
        </td>
    </tr>
</table>`;

export var email_two_col_text = `
<table cellpadding="0" cellspacing="0" width="100%" border="0">
    <tr>
        <td style="padding: 15px 10px;" valign="middle">
            <table cellpadding="0" cellspacing="0" width="290" border="0" style="float: right;">
                <tr>
                    <td style="padding:5px 0 5px 5px;">
                        <h3 style="color: #444">{{heading_1}}</h3>
                        <p style="font-size: 14px;color: #444">{{html_text_1}}</p>
                    </td>
                </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="290" border="0" style="float: right;">
                <tr>
                    <td style="padding:5px 0 5px 5px;">
                        <h3 style="color: #444">{{heading_2}}</h3>
                        <p style="font-size: 14px;color: #444">{{html_text_2}}</p>
                    </td>
                </tr>
            </table>    
        </td>
    </tr>
</table>`;
export var image_three_side = `
<div class="middle_contain_wrap">
    <section>
        <div class="top_productrow">
            <div class="cus_container">
                <div class="row">
                    <div class="col-12 col-lg-4">
                        <div class="top_productbox">
                            <a href="#"><img src="{{box1_img}}" alt=""></a>
                        </div>
        
                    </div>
                    <div class="col-12 col-lg-4">
                        <div class="top_productbox">
                            <a href="#"><img src="{{box2_img}}" alt=""></a>
                        </div>
                    </div>
                    <div class="col-12 col-lg-4">
                        <div class="top_productbox">
                            <a href="#"><img src="{{box3_img}}" alt=""></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section></div>`;

    