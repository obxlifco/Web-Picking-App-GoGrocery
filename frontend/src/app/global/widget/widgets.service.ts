import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable, Inject} from '@angular/core'; 
import { CookieService} from 'ngx-cookie';
import { GlobalVariable} from '../service/global';
import { GlobalService } from '../service/app.global.service';
import {CategoryService} from '../service/category.service';
import {Widget} from './widget';
import * as templates from './widget-templates';

import {BannerComponent, InfoboxComponent, VFeaturedBoxComponent, HFeaturedBoxComponent, FeatureProductComponent,BrandsWidgetComponent,CategoriesComponent,ParentCategoriesComponent,NewProductComponent, BestSellerProductComponent, FreeTextComponent, TwoColumnTextComponent, ThreeColumnTextComponent, ImageWithTextComponent, TwoSideBannerComponent, HeadingTextComponent, FormComponent, ThreeSideBannerComponent,IntroComponent,AboutSectionComponent,EmailBannerComponent,EmailTwoSideBannerComponent,EmailHeadingTextComponent,PaymentImage,EmailImageWithTextComponent,EmailImageWithTwoTextComponent,EmailFreeTextComponent,EmailTwoColumnTextComponent,EmailTwoProductComponent,EmailSeparatorComponent,EmailFourProductComponent,EmailButtonComponent,EmailButtonTwoComponent,AllProductConditionWise,CarouselComponent,BestSellOrDealProduct,SubscribeNewsLetter,OurFeature,CategoryBanner,PromotionBanner} from '../../modules/cms/widgets/cms.widgets.component';
import { WINDOW } from '@ng-toolkit/universal';

@Injectable({
   providedIn: 'root'
})
export class WidgetsService {
  public components:any;
  public rootURI:string;
  public picRootURI:string;
  public cdnRootUrl:string = 'https://d2vltvjwlghbux.cloudfront.net/frontend';
  public parentCategoryList = [];
  public categoryBannerList = [];
  public promotionBannerList = [];
  public shopByCategoryData  = [];
  public brandList = [];

  constructor(@Inject(WINDOW) private window: Window, private _http: Http,private _globalService:GlobalService,private _cookieService:CookieService,private _categoryService : CategoryService) { 
    this.rootURI = this.window.location.origin+'/'+this.window.location.pathname.split('/')[1];
    this.picRootURI = this.window.location.origin;
    this.components = { 
      //CMS COMPONENTS
      BannerComponent: BannerComponent,
      CarouselComponent : CarouselComponent,
      InfoboxComponent: InfoboxComponent,
      VFeaturedBoxComponent: VFeaturedBoxComponent,
      HFeaturedBoxComponent: HFeaturedBoxComponent,
      FeatureProductComponent: FeatureProductComponent,
      CategoriesComponent: CategoriesComponent,
      ParentCategoriesComponent:ParentCategoriesComponent,
      BrandsWidgetComponent:BrandsWidgetComponent,
      NewProductComponent: NewProductComponent,
      BestSellerProductComponent: BestSellerProductComponent,
      FreeTextComponent: FreeTextComponent,
      TwoColumnTextComponent: TwoColumnTextComponent,
      ThreeColumnTextComponent: ThreeColumnTextComponent,
      ImageWithTextComponent: ImageWithTextComponent,
      PaymentImage:PaymentImage,
      TwoSideBannerComponent: TwoSideBannerComponent,
      HeadingTextComponent: HeadingTextComponent,
      FormComponent: FormComponent,
      BestSellOrDealProduct : BestSellOrDealProduct,
      ThreeSideBannerComponent: ThreeSideBannerComponent,
      IntroComponent: IntroComponent,
      AboutSectionComponent:AboutSectionComponent,
      AllProductConditionWise:AllProductConditionWise,
      OurFeature:OurFeature,
      CategoryBanner:CategoryBanner,
      PromotionBanner:PromotionBanner,
      //NEWSLETTER COMPONENTS
      SubscribeNewsLetter:SubscribeNewsLetter,
      EmailBannerComponent,
      EmailTwoSideBannerComponent,
      EmailHeadingTextComponent,
      EmailImageWithTextComponent,
      EmailImageWithTwoTextComponent,
      EmailFreeTextComponent,
      EmailTwoColumnTextComponent,
      EmailTwoProductComponent,
      EmailSeparatorComponent,
      EmailFourProductComponent,
      EmailButtonComponent,
      EmailButtonTwoComponent
    };
    this._categoryService.getParentCategoryList().subscribe(response => {
      this.parentCategoryList = response && response['status'] == 1 ? response['data'] : [];
      console.log("************** Parent category list ***************")
      console.log(this.parentCategoryList);
    });
    this._categoryService.getCategoryBannerList().subscribe(response => {
      this.categoryBannerList = response && response['status'] == 1 ? response['data'] : [];
      
    });
    this._categoryService.getPromotionsBanner().subscribe(response => {
      this.promotionBannerList = response && response['status'] == 200 ? response['data'] : [];
      console.log("**************** Promotion banner data **************");
      console.log(this.promotionBannerList);
     
    });
    this._categoryService.getShopByCategoryData().subscribe(response => {
     this.shopByCategoryData = response && response['status'] == 1 ? response['data'] : [];
    });
    // Get brand list
   /* this._categoryService.getBrandList().subsribe(response => {
      this.brandList = response && response['status'] == 1 ? response['data'] : [];

    });*/
    this._categoryService.getBrands().subscribe(response => {
      this.brandList = response && response['status'] == 1 ? response['brands'] : [];
    });

  }

  widgetList(){
    var widgets = [];
    //type: 1-other, 2-editor 3-form
    //is_distributor 1-company, 2-distributor, 3-all
    //widgets.push(new Widget(1, 3,2,"Banner", 1, "icon-banner", 'BannerComponent',templates.banner,[{'label': 'Upload Image', 'properties': [{ 'label':'Banner Image URL', 'selector': 'banner_url', 'value': this.cdnRootUrl+'/assets/images/home_ban-min.jpg','is_hint': false,'hint_text':'','is_file':true,'type':0,'image_size': { width: 1920, height: 630 } },{ 'label':'Image Title','selector': 'banner_alt', 'value': 'Banner','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'banner_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Banner Text', 'properties': [{ 'label':'Heading', 'selector': 'banner_heading', 'field':'editor', 'value': 'Banner Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'banner_sub_heading', 'field':'editor','value': 'Banner Sub Heading','is_hint': false,'hint_text':'','is_file':false }]}]));
    widgets.push(new Widget(1, 3,2,"Banner", 1, "icon-pic", 'BannerComponent',templates.banner,[{'label': 'Upload Image', 'properties': [{ 'label':'Banner Image URL', 'selector': 'banner_url', 'value': '/assets/images/home_image.png','is_hint': false,'hint_text':'','is_file':true,'type':0,'image_size': { width: 1920, height: 630 } },{ 'label':'Image Title','selector': 'banner_alt', 'value': 'Banner','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'banner_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Banner Text', 'properties': [{ 'label':'Heading', 'selector': 'banner_heading', 'field':'editor', 'value': 'Banner Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'banner_sub_heading', 'field':'editor','value': 'Banner Sub Heading','is_hint': false,'hint_text':'','is_file':false }]}]));
    widgets.push(new Widget(2, 3,6,"Information Box", 1, "fa fa-info", 'InfoboxComponent',templates.info_box,[{ 'label': 'First', 'properties':[{ 'label':'Heading', 'selector': 'heading1', 'value': 'FREE SHIPPING','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'desc1', 'value': 'Free shipping for all orders','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Icon', 'selector': 'icon1', 'value': 'fa-truck','is_hint': true,'hint_text':'Font Awesome icon class, e.g fa-truck','is_icon':true,'is_file':false }]},{ 'label': 'Second', 'properties': [{ 'label':'Heading', 'selector': 'heading2', 'value': 'SUPPORT 24/7','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'desc2', 'value': 'We support 24 hour of day','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Icon', 'selector': 'icon2', 'value': 'fa-life-ring','is_hint': true,'hint_text':'Font Awesome icon class, e.g fa-truck','is_icon':true,'is_file':false }]},{ 'label': 'Third', 'properties': [{ 'label':'Heading', 'selector': 'heading3', 'value': '30 day Return','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'desc3', 'value': 'You have 30 days to return','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Icon', 'selector': 'icon3', 'value': 'fa-retweet','is_hint': true,'hint_text':'Font Awesome icon class, e.g fa-truck','is_icon':true,'is_file':false }]}, { 'label': 'Fourth', 'properties': [{ 'label':'Heading', 'selector': 'heading4', 'value': 'Payment 100% Secure','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'desc4', 'value': 'You are secured','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Icon', 'selector': 'icon4', 'value': 'fa-credit-card','is_hint': true,'hint_text':'Font Awesome icon class, e.g fa-truck','is_icon':true,'is_file':false }]} ]));

   // widgets.push(new Widget(3, 1,2,"Three Side Banner", 1, "icon-three-side-banner", 'VFeaturedBoxComponent',templates.featured_box_v,[{'label':'First Image', 'properties': [{ 'label':'Image', 'selector': 'box1_img', 'value': this.cdnRootUrl+'/assets/images/pro_3.jpg','is_hint': false,'hint_text':'','is_file': true,'type':0,'image_size': { width: 370, height: 515 } },{ 'label':'Title','selector': 'box1_heading', 'value': 'FESTIVE FEELS','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Title','selector': 'box1_text', 'value': 'Donec dolor lectus','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box1_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{ 'label': 'Second Image', 'properties': [{ 'label':'Image', 'selector': 'box2_img', 'value': this.cdnRootUrl+'/assets/images/pro_4.jpg','is_hint': false,'hint_text':'', 'is_file': true,'type':0,'image_size': { width: 370, height: 515 } },{ 'label':'Title','selector': 'box2_heading', 'value': 'TOP SALES','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Title','selector': 'box2_text', 'value': 'Donec dolor lectus','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box2_url', 'value': this.rootURI,'is_hint': false,'hint_text':'', 'is_file':false }]},{ 'label': 'Third Image', 'properties': [{ 'label':'Image', 'selector': 'box3_img', 'value': this.cdnRootUrl+'/assets/images/pro_5.jpg','is_hint': false,'hint_text':'', 'is_file': true, 'type':0,'image_size': { width: 370, height: 515 } },{ 'label':'Title','selector': 'box3_heading', 'value': 'RECENT COLLECTIONS','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Title','selector': 'box3_text', 'value': 'Donec dolor lectus','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box1_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));

    //widgets.push(new Widget(4, 1,2, "Two Side Image With Text", 1, "icon-two-side-image", 'HFeaturedBoxComponent',templates.featured_box_h,[{'label':'First Image', 'properties':[{'label':'Image', 'selector': 'box1_img', 'value': this.cdnRootUrl+'/assets/images/pro_1.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 610, height: 330 } },{'label':'Heading', 'selector': 'box1_heading', 'value': 'Sale upto 50% OFF','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'box1_desc', 'value': 'Ut enim ad minim veniam quis nostrud exercitation.','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Button','selector': 'box1_btn', 'value': 'SHOP NOW','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box1_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Second Image', 'properties': [{'label':'Image', 'selector': 'box2_img', 'value': this.cdnRootUrl+'/assets/images/pro_2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 610, height: 330 } },{'label':'Heading', 'selector': 'box2_heading', 'value': 'Accessories Collections','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'box2_desc', 'value': 'Ut enim ad minim veniam quis nostrud exercitation.','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Button','selector': 'box2_btn', 'value': 'SHOP NOW','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box2_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));

   // widgets.push(new Widget(5, 3,4,"Feauture Product", 1, "icon-folder", 'FeatureProductComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Feauture Product','is_hint': false,'hint_text':'','is_file':false }] }]));

   // widgets.push(new Widget(6, 3,4,"New Arrivals", 1, "icon-folder", 'NewProductComponent',templates.product_list,[{'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'New Arrivals','is_hint': false,'hint_text':'','is_file':false }]}]));    

   // widgets.push(new Widget(7, 3,4,"Best Sellers", 1, "icon-folder", 'BestSellerProductComponent',templates.product_list,[{'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Best Sellers','is_hint': false,'hint_text':'','is_file':false }]}]));  
 
    widgets.push(new Widget(8, 3,3,"Single Column Layout Text", 2, "icon-letter-t", 'FreeTextComponent',templates.single_column_layout_text,[{'label':'Properties','properties':[{ 'label':'HTML Text', 'selector': 'html_text', 'value': '<p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>','is_hint': false,'hint_text':'','is_file':false }]}]));        

    widgets.push(new Widget(9, 3,3,"Two Column Layout Text", 1, "icon-letter-t", 'TwoColumnTextComponent',templates.two_column_layout_text,[{'label':'First Column','properties':[{ 'label':'Heading', 'selector': 'heading_1','value': 'Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Text Content', 'selector': 'html_text_1', 'field':'editor', 'value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]},{'label':'Second Column','properties':[{ 'label':'Heading', 'selector': 'heading_2', 'value': 'Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Text Content', 'selector': 'html_text_2', 'field':'editor','value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]}]));

    widgets.push(new Widget(10, 3,3,"Three Column Layout Text", 1, "icon-letter-t", 'ThreeColumnTextComponent',templates.three_column_layout_text,[{'label':'First Column','properties':[{ 'label':'Heading', 'selector': 'heading_1', 'value': 'Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Text Content', 'selector': 'html_text_1', 'field':'editor', 'value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]},{'label':'Second Column','properties':[{ 'label':'Heading', 'selector': 'heading_2', 'value': 'Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Text Content', 'selector': 'html_text_2', 'field':'editor','value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]},{'label':'Third Column','properties':[{ 'label':'Heading', 'selector': 'heading_3', 'value': 'Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Text Content', 'selector': 'html_text_3', 'field':'editor','value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]}]));     
    widgets.push(new Widget(11, 3,2, "Image With Text", 1, "icon-image-with-text", 'ImageWithTextComponent',templates.image_with_text,[{'label':'Image', 'properties':[{'label':'Image', 'selector': 'img', 'value': this.cdnRootUrl+'/assets/images/pro_1.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Image Title', 'selector': 'img_alt', 'value': '','is_hint': false,'hint_text':'','is_file':false },{'label':'Image Align', 'selector': 'img_align', 'value': 'left','is_hint': true,'hint_text':'Type Left or Right','is_file':false }]},{'label': 'Text Content', 'properties': [{'label':'Heading', 'selector': 'heading', 'value': 'Accessories Collections','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Description','selector': 'desc_text', 'field':'editor','value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]}]));   
    //widgets.push(new Widget(12, 3,2, "Two Side Banner", 1, "icon-two-side-banner", 'TwoSideBannerComponent',templates.two_side_banner,[{'label':'First Banner', 'properties':[{'label':'Image', 'selector': 'box1_img', 'value': this.cdnRootUrl+'/assets/images/pro_1.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 610, height: 330 } },{'label':'Image Title', 'selector': 'box1_alt', 'value': 'Sale upto 50% OFF','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box1_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Second Banner', 'properties': [{'label':'Image', 'selector': 'box2_img', 'value': this.cdnRootUrl+'/assets/images/pro_2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 610, height: 330 } },{'label':'Image Title', 'selector': 'box2_alt', 'value': 'Accessories Collections','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box2_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));
    widgets.push(new Widget(13, 3,3,"Heading", 1, "icon-letter-t", 'HeadingTextComponent',templates.heading_text,[{ 'label':'Properties','properties':[{ 'label':'Heading Text', 'selector': 'heading_text', 'value': 'Heading Text','is_hint': false,'hint_text':'','is_file':false }] }]));
    widgets.push(new Widget(14, 3,6,"Form", 3, "icon-paper-1", 'FormComponent',templates.default_form,[{'submit_url':'/','submit_button_text':'Submit','reset_button_text':'Reset','fields':[{ 'custom_values':"",'default_values':"",'field_label':"Full Name",'input_type':"Textbox",'value_required':"y"},{ 'custom_values':"",'default_values':"",'field_label':"Email",'input_type':"Email",'value_required':"y"},{ 'custom_values':"",'default_values':"",'field_label':"Mobile",'input_type':"Phone",'value_required':"y"},{ 'custom_values':"male,female",'default_values':"",'field_label':"Gender",'input_type':"Radio",'value_required':"n"},{ 'custom_values':"India,Usa,Thailand,Uk",'default_values':"",'field_label':"Country",'input_type':"Dropdown",'value_required':"n"}]}]));
    //widgets.push(new Widget(15, 3,2,"Three Side Banner Image", 1, "icon-three-side-banner", 'ThreeSideBannerComponent',templates.featured_box_v,[{'label':'First Image', 'properties': [{ 'label':'Image', 'selector': 'box1_img', 'value': this.cdnRootUrl+'/assets/images/smallbanner1.jpg','is_hint': false,'hint_text':'','is_file': true,'type':0,'image_size': { width: 376, height: 220 } },{ 'label':'Link','selector': 'box1_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{ 'label': 'Second Image', 'properties': [{ 'label':'Image', 'selector': 'box2_img', 'value': this.cdnRootUrl+'/assets/images/smallbanner2.jpg','is_hint': false,'hint_text':'', 'is_file': true,'type':0,'image_size': { width: 376, height: 220 } },{ 'label':'Link','selector': 'box2_url', 'value': this.rootURI,'is_hint': false,'hint_text':'', 'is_file':false }]},{ 'label': 'Third Image', 'properties': [{ 'label':'Image', 'selector': 'box3_img', 'value': this.cdnRootUrl+'/assets/images/smallbanner3.jpg','is_hint': false,'hint_text':'', 'is_file': true, 'type':0,'image_size': { width: 376, height: 220 } },{ 'label':'Link','selector': 'box1_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));
   // widgets.push(new Widget(16, 3,2,"Intro Section", 1, "icon-image-with-text", 'IntroComponent',templates.featured_box_v,[{'label':'Properties', 'properties': [{ 'label':'Image', 'selector': 'box_img', 'value': this.cdnRootUrl+'/assets/images/dist_2.jpg','is_hint': false,'hint_text':'','is_file': true,'type':0,'image_size': { width: 570, height: 400 } },{ 'label':'Heading','selector': 'heading', 'value': 'INTRODUCING','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'sub_heading', 'value': 'Donec dolor lectus','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Description','selector': 'description', 'field':'editor','value': 'Quisque non tortor facilisis, auctor risus et, tristique arcu. Nam gravida consequat dolor, in euismod purus cursus vitae. In a porttitor dui, sit amet cursus sapien. Pellentesque ac laoreet quam, nec convallis eros. Vestibulum non ipsum vel orci ullamcorper lobortis ultricies a mauris. Proin lobortis lacus sed tortor suscipit, in auctor mi blandit.','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Button Text','selector': 'button_text', 'value': 'Explore','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'button_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));  
    //widgets.push(new Widget(17, 3,2, "About Section", 1, "icon-image-with-text", 'AboutSectionComponent',templates.two_side_banner,[{'label':'First Banner', 'properties':[{'label':'Image', 'selector': 'box1_img', 'value': this.cdnRootUrl+'/assets/images/dist_2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 275 } },{ 'label':'Link','selector': 'box1_img_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Second Banner', 'properties': [{'label':'Image', 'selector': 'box2_img', 'value': this.cdnRootUrl+'/assets/images/dist_1.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 540 } },{ 'label':'Link','selector': 'box2_img_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Third Banner', 'properties': [{'label':'Image', 'selector': 'box3_img', 'value': this.cdnRootUrl+'/assets/images/dist_2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 275 } },{ 'label':'Link','selector': 'box3_img_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Text Content', 'properties': [{ 'label':'Heading','selector': 'box_heading', 'value': 'INTRODUCING','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Description','selector': 'box_description', 'field':'editor','value': 'Quisque non tortor facilisis, auctor risus et, tristique arcu. Nam gravida consequat dolor, in euismod purus cursus vitae. In a porttitor dui, sit amet cursus sapien. Pellentesque ac laoreet quam, nec convallis eros. Vestibulum non ipsum vel orci ullamcorper lobortis ultricies a mauris. Proin lobortis lacus sed tortor suscipit, in auctor mi blandit.','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Button Text','selector': 'btn_text', 'value': 'Read More','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Button Link','selector': 'btn_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));  
    //widgets.push(new Widget(18, 3,4,"Brands", 1, "icon-folder-open", 'BrandsWidgetComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Brands','is_hint': false,'hint_text':'','is_file':false }] }]));
    widgets.push(new Widget(19, 3,4,"Categories", 1, "icon-folder-open", 'CategoriesComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Categories','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_1','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_2','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_3','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_4','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_5','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_6','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_7','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category', 'selector': 'category_id_8','selector_key_name':'name','value':'','options': this.shopByCategoryData,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_multiple':true,'is_hint': false,'hint_text':'','is_file':false }] }]));
    widgets.push(new Widget(20, 3,4,"Parent Categories Product", 1, "icon-folder-open", 'ParentCategoriesComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Parent Categories Product','is_hint': false,'hint_text':'','is_file':false},{ 'label':'Select Category', 'selector': 'category_id','selector_key_name':'name','value':'','options': this.parentCategoryList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false }] }]));
    widgets.push(new Widget(29, 1,2,"Category Banner", 1, "icon-images", 'CategoryBanner',templates.category_banner,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Category Banner','is_hint': false,'hint_text':'','is_file':false},{ 'label':'Select Category', 'selector': 'category_banner_id_1','selector_key_name':'banner_name','value':'','object_for':'category_banner','options': this.categoryBannerList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category','selector_key_name':'banner_name','object_for':'category_banner','selector': 'category_banner_id_2','value':'','options': this.categoryBannerList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Category','selector_key_name':'banner_name','object_for':'category_banner','selector': 'category_banner_id_3','value':'','options': this.categoryBannerList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false }] }]));
    widgets.push(new Widget(30, 1,2,"Promotion Banner", 1, "icon-images", 'PromotionBanner',templates.promotion_banner,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Promotion Banner','is_hint': false,'hint_text':'','is_file':false},{ 'label':'Select Banner', 'selector': 'category_banner_id_1','selector_key_name':'banner_name','value':'','object_for':'category_banner','options': this.promotionBannerList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Banner','selector_key_name':'banner_name','object_for':'category_banner','selector': 'category_banner_id_2','value':'','options': this.promotionBannerList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Banner','selector_key_name':'banner_name','object_for':'category_banner','selector': 'category_banner_id_3','value':'','options': this.promotionBannerList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false }] }]));
    widgets.push(new Widget(18, 3,4,"Brands", 1, "icon-images", 'BrandsWidgetComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Brands','is_hint': false,'hint_text':'','is_file':false},{ 'label':'Select Brands', 'selector': 'brand_id_1','selector_key_name':'name','value':'','object_for':'brand','options': this.brandList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Brand','selector_key_name':'name','object_for':'brand','selector': 'brand_id_2','value':'','options': this.brandList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Brand','selector_key_name':'name','object_for':'brand','selector': 'brand_id_3','value':'','options': this.brandList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Brand','selector_key_name':'name','object_for':'brand','selector': 'brand_id_4','value':'','options': this.brandList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Select Brand','selector_key_name':'name','object_for':'brand','selector': 'brand_id_5','value':'','options': this.brandList,'chnageThisValueToOtherSelector' : ['heading_text'],'field':'selectbox','is_hint': false,'hint_text':'','is_file':false }] }]));
   // widgets.push(new Widget(21, 3,4,"Food & Beverages", 1, "icon-folder", 'ParentCategoriesComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Food & Beverages','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Heading', 'selector': 'category_id', 'value': 2,'is_hint': false,'hint_text':'','is_file':false }] }]));
    //widgets.push(new Widget(22, 3,4,"Staples", 1, "icon-folder", 'ParentCategoriesComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Staples','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Heading', 'selector': 'category_id', 'value': 70,'is_hint': false,'hint_text':'','is_file':false }] }]));
    //widgets.push(new Widget(23, 3,4,"Bakery Store", 1, "icon-folder", 'ParentCategoriesComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Bakery Store','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Heading', 'selector': 'category_id', 'value': 76,'is_hint': false,'hint_text':'','is_file':false }] }]));
    widgets.push(new Widget(24, 3,4,"Three Column With Discount", 1, "icon-folder-open", 'AllProductConditionWise',templates.image_three_side,[{'label':'First Banner', 'properties':[{'label':'Image', 'selector': 'box1_img', 'value':'/assets/images/Group_39.png','is_hint': false,'hint_text':'','is_file':true, 'type':0 },{ 'label':'Link','selector': 'box1_img_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Second Banner', 'properties': [{'label':'Image', 'selector': 'box2_img', 'value': '/assets/images/Group_39.png','is_hint': false,'hint_text':'','is_file':true, 'type':0 },{ 'label':'Link','selector': 'box2_img_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Third Banner', 'properties': [{'label':'Image', 'selector': 'box3_img', 'value': '/assets/images/Group_39.png','is_hint': false,'hint_text':'','is_file':true, 'type':0},{ 'label':'Link','selector': 'box3_img_url', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));  
    widgets.push(new Widget(11, 3,2, "Payment Image", 1, "icon-image-with-text", 'PaymentImage',templates.image_with_text,[{'label':'Image', 'properties':[{'label':'Image', 'selector': 'img', 'value': '/assets/images/payment_home.png','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Image Title', 'selector': 'img_alt', 'value': '','is_hint': false,'hint_text':'','is_file':false },{'label':'Image Align', 'selector': 'img_align', 'value': 'left','is_hint': true,'hint_text':'Type Left or Right','is_file':false }]},{'label': 'Text Content', 'properties': [{'label':'Heading', 'selector': 'heading', 'value': 'Accessories Collections','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Description','selector': 'desc_text', 'field':'editor','value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]}]));   
    //widgets.push(new Widget(23, 3,4,"Detergents & Cleanings", 1, "icon-folder", 'ParentCategoriesComponent',templates.product_list,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Detergents & Cleanings','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Heading', 'selector': 'category_id', 'value': 152,'is_hint': false,'hint_text':'','is_file':false }] }]));
    // Deals of the day
     widgets.push(new Widget(25, 3,4,"Deals of the Day", 1, "icon-folder-open", 'BestSellOrDealProduct',templates.sell_or_deal_prduct,[{ 'label':'Properties','product_type' : 'best_deals','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Deals Of The Day','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Heading', 'selector': 'category_id', 'value': 152,'is_hint': false,'hint_text':'','is_file':false }] }]));
    // Best selling products
     widgets.push(new Widget(26, 3,4,"Best Selling Products", 1, "icon-folder-open", 'BestSellOrDealProduct',templates.sell_or_deal_prduct,[{ 'label':'Properties','product_type': 'best_sell','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Best Selling Products','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Heading', 'selector': 'category_id', 'value': 152,'is_hint': false,'hint_text':'','is_file':false }] }]));
     widgets.push(new Widget(27, 3,3,"Subscribe To Newsletter", 1, "icon-folder-open", 'SubscribeNewsLetter',templates.subscribenewsletter,[{ 'label':'Properties','properties':[{ 'label':'Heading', 'selector': 'heading_text', 'value': 'Subscribe our newsletter to get the best offers and latest deals!','is_hint': false,'hint_text':'','is_file':false }] }]));
     // Our Feature
     widgets.push(new Widget(28, 3,3,"Our Feature",4, "icon-folder-open", 'OurFeature',templates.OurFeature,[{ 'label':'Properties','properties': [
                                                                                                                                            {
                                                                                                                                            'label': 'Icon',
                                                                                                                                            'selector': 'our_feature_icon_1',
                                                                                                                                            'value': '',
                                                                                                                                            'is_hint': false,
                                                                                                                                            'hint_text': '',
                                                                                                                                            'is_file': false,
                                                                                                                                            'type': 0,
                                                                                                                                            'is_icon': true,
                                                                                                                                            'associative_fields': [
                                                                                                                                            {
                                                                                                                                              'label': 'Feature Title',
                                                                                                                                              'selector': 'our_feature_title_1',
                                                                                                                                              'value': 'Test Feature Title',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            },
                                                                                                                                            {
                                                                                                                                              'label': 'Feature Description',
                                                                                                                                              'selector': 'our_feature_description_1',
                                                                                                                                              'value': 'Test Description',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            }
                                                                                                                                            ]
                                                                                                                                            },
                                                                                                                                            {
                                                                                                                                            'label': 'Icon',
                                                                                                                                            'selector': 'our_feature_icon_2',
                                                                                                                                            'value': '',
                                                                                                                                            'is_hint': false,
                                                                                                                                            'hint_text': '',
                                                                                                                                            'is_file': false,
                                                                                                                                            'type': 0,
                                                                                                                                            'is_icon': true,
                                                                                                                                            'associative_fields': [
                                                                                                                                            {
                                                                                                                                              'label': 'Feature Title',
                                                                                                                                              'selector': 'our_feature_title_2',
                                                                                                                                              'value': 'Our Feature Title 2',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            },
                                                                                                                                            {
                                                                                                                                              'label': 'Feature Description',
                                                                                                                                              'selector': 'our_feature_description_1',
                                                                                                                                              'value': 'TEST DESCRIPTION2',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            }
                                                                                                                                            ]
                                                                                                                                            },
                                                                                                                                            {
                                                                                                                                            'label': 'Icon',
                                                                                                                                            'selector': 'our_feature_icon_3',
                                                                                                                                            'value': '',
                                                                                                                                            'is_hint': false,
                                                                                                                                            'hint_text': '',
                                                                                                                                            'is_file': false,
                                                                                                                                            'type': 0,
                                                                                                                                            'is_icon': true,
                                                                                                                                            'associative_fields': [
                                                                                                                                            {
                                                                                                                                              'label': 'Feature Title',
                                                                                                                                              'selector': 'our_feature_title_3',
                                                                                                                                              'value': 'Our Feature Title 3',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            },
                                                                                                                                            {
                                                                                                                                              'label': 'Image description 3',
                                                                                                                                              'selector': 'carousel_image_description3',
                                                                                                                                              'value': 'Carousel image description3',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            }
                                                                                                                                            ]
                                                                                                                                            },
                                                                                                                                            {
                                                                                                                                            'label': 'Icon',
                                                                                                                                            'selector': 'our_feature_icon_4',
                                                                                                                                            'value': '',
                                                                                                                                            'is_hint': false,
                                                                                                                                            'hint_text': '',
                                                                                                                                            'is_file': false,
                                                                                                                                            'type': 0,
                                                                                                                                            'is_icon': true,
                                                                                                                                            'associative_fields': [
                                                                                                                                            {
                                                                                                                                              'label': 'Feature Title',
                                                                                                                                              'selector': 'our_feature_title_4',
                                                                                                                                              'value': 'Test Feature Title',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            },
                                                                                                                                            {
                                                                                                                                              'label': 'Feature Description',
                                                                                                                                              'selector': 'our_feature_description_4',
                                                                                                                                              'value': 'Test Description',
                                                                                                                                              'is_hint': false,
                                                                                                                                              'hint_text': '',
                                                                                                                                              'is_file': false
                                                                                                                                            }
                                                                                                                                            ]
                                                                                                                                            }
                                                                                                                                            ]
                                                                                                                                            }]));

    // Widget for slider
     widgets.push(new Widget(24,1,2,'CAROUSEL',4,'fa fa-sliders','CarouselComponent',templates.carousel,[{'label' : 'Carousel Images','add_more':true,'maximum_item':12,'default_object' :'carousel_default_object','properties':[{

                                                                                                                                        'label':'Carousel Image Url',
                                                                                                                                        'selector':'carousel_image_url_1',
                                                                                                                                        'value': '/assets/images/carousel_image_1.png',
                                                                                                                                        'is_hint' : false,
                                                                                                                                        'hint_text':'',
                                                                                                                                        'is_file':true,
                                                                                                                                        'type' : 0,
                                                                                                                                        'image_size':{'width':1920,height:630},
                                                                                                                                        'is_icon' : false,
                                                                                       
                                                                                                                                      'associative_fields' : [{
                                                                                                                                        'label':'Image Caption 1',
                                                                                                                                        'selector': 'carousel_image_caption_1',
                                                                                                                                        'value': 'Image Caption 1',
                                                                                                                                        'is_hint': false,
                                                                                                                                        'hint_text':'',
                                                                                                                                        'is_file':false
                                                                                                                                      },
                                                                                                                                      {
                                                                                                                                        'label':'Image description 1',
                                                                                                                                        'selector':'carousel_image_description1',
                                                                                                                                        'value' : 'Carousel image description',
                                                                                                                                        'is_hint' : false,
                                                                                                                                        'hint_text' : '',
                                                                                                                                        'is_file' : false
                                                                                                                                      }
                                                                                                                                     ]
                                                                                                                                    },
                                                                                                                                    {
                                                                                                                        
                                                                                                                                        'label':'Carousel Image Url',
                                                                                                                                        'selector':'carousel_image_url_2',
                                                                                                                                        'value': '/assets/images/carousel_image_2.png',
                                                                                                                                        'is_hint' : false,
                                                                                                                                        'hint_text':'',
                                                                                                                                        'is_file':true,
                                                                                                                                        'type' : 0,
                                                                                                                                        'image_size':{'width':1920,height:630},
                                                                                                                                        'is_icon' : false,
                                                                                               
                                                                                                                                      'associative_fields' : [{
                                                                                                                                        'label':'Image Caption 2',
                                                                                                                                        'selector': 'carousel_image_caption_2',
                                                                                                                                        'value': 'Image Caption 2',
                                                                                                                                        'is_hint': false,
                                                                                                                                        'hint_text':'',
                                                                                                                                        'is_file':false
                                                                                                                                      },
                                                                                                                                      {
                                                                                                                                        'label':'Image description 2',
                                                                                                                                        'selector':'carousel_image_description2',
                                                                                                                                        'value' : 'Carousel image description2',
                                                                                                                                        'is_hint' : false,
                                                                                                                                        'hint_text' : '',
                                                                                                                                        'is_file' : false
                                                                                                                                      }
                                                                                                                                    ]
                                                                                                                                  },
                                                                                                                                    {
                                                                                                                                      
                                                                                                                                        'label':'Carousel Image Url',
                                                                                                                                        'selector':'carousel_image_url_3',
                                                                                                                                        'value': '/assets/images/carousel_image_3.png',
                                                                                                                                        'is_hint' : false,
                                                                                                                                        'hint_text':'',
                                                                                                                                        'is_file':true,
                                                                                                                                        'type' : 0,
                                                                                                                                        'image_size':{'width':1920,height:630},
                                                                                                                                        'is_icon' : false,
                                                         
                                                                                                                                      'associative_fields' : [{
                                                                                                                                        'label':'Image Caption 3',
                                                                                                                                        'selector': 'carousel_image_caption_3',
                                                                                                                                        'value': 'Image Caption 3',
                                                                                                                                        'is_hint': false,
                                                                                                                                        'hint_text':'',
                                                                                                                                        'is_file':false
                                                                                                                                      },
                                                                                                                                      {
                                                                                                                                        'label':'Image description 3',
                                                                                                                                        'selector':'carousel_image_description3',
                                                                                                                                        'value' : 'Carousel image description3',
                                                                                                                                        'is_hint' : false,
                                                                                                                                        'hint_text' : '',
                                                                                                                                        'is_file' : false
                                                                                                                                      }]
                                                                                                                                    }]}]));
    return widgets;
  }

  widgetListEmail(){
      var widgets = [];
      //type: 1-other, 2-editor, 3- form
      widgets.push(new Widget(1, 3,2,"Banner", 1, "icon-pic", 'EmailBannerComponent',templates.email_banner,[{'label': 'Upload Image', 'properties': [{ 'label':'Banner Image URL', 'selector': 'banner_url', 'value': this.cdnRootUrl+'/assets/images/banner.jpg','is_hint': false,'hint_text':'','is_file':true,'type':0,'image_size': { width: 1920, height: 630 } },{ 'label':'Image Title','selector': 'banner_alt', 'value': 'Banner','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'banner_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));

      widgets.push(new Widget(2, 3,2, "Two Side Banner", 1, "icon-two-side-banner", 'EmailTwoSideBannerComponent',templates.email_two_side_banner,[{'label':'First Banner', 'properties':[{'label':'Image', 'selector': 'box1_img', 'value': this.cdnRootUrl+'/assets/images/img1.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Image Title', 'selector': 'box1_alt', 'value': 'Sale upto 50% OFF','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box1_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Second Banner', 'properties': [{'label':'Image', 'selector': 'box2_img', 'value': this.cdnRootUrl+'/assets/images/img1.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Image Title', 'selector': 'box2_alt', 'value': 'Accessories Collections','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box2_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));
     
      widgets.push(new Widget(3, 3,3,"Heading Text", 1, "icon-text-heading", 'EmailHeadingTextComponent',templates.email_heading_text,[{ 'label':'Properties','properties':[{ 'label':'Heading Text', 'selector': 'heading_text', 'value': 'Heading Text','is_hint': false,'hint_text':'','is_file':false }] }]));

      widgets.push(new Widget(4, 3,2, "Image With Text", 1, "icon-image-with-text", 'EmailImageWithTextComponent',templates.email_image_with_text,[{'label':'Image', 'properties':[{'label':'Image', 'selector': 'img', 'value': this.cdnRootUrl+'/assets/images/img1.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Image Title', 'selector': 'img_alt', 'value': '','is_hint': false,'hint_text':'','is_file':false },{'label':'Image Align', 'selector': 'img_align', 'value': 'left','is_hint': true,'hint_text':'Left or Right','is_file':false }]},{'label': 'Text Content', 'properties': [{'label':'Heading', 'selector': 'heading', 'value': 'Accessories Collections','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Description','selector': 'desc_text', 'field':'editor','value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]}]));

      widgets.push(new Widget(5, 3,2, "Two Side Image With Text", 1, "icon-two-side-image", 'EmailImageWithTwoTextComponent',templates.email_two_side_img_text,[{'label':'First Image', 'properties':[{'label':'Image', 'selector': 'box1_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Heading', 'selector': 'box1_heading', 'value': 'Sale upto 50% OFF','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'box1_desc', 'value': 'Ut enim ad minim veniam quis nostrud exercitation.','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box1_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label': 'Second Image', 'properties': [{'label':'Image', 'selector': 'box2_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Heading', 'selector': 'box2_heading', 'value': 'Accessories Collections','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Sub Heading','selector': 'box2_desc', 'value': 'Ut enim ad minim veniam quis nostrud exercitation.','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Link','selector': 'box2_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));
     
      widgets.push(new Widget(6, 3,3,"Single Column Layout Text", 2, "icon-text-box-tool", 'EmailFreeTextComponent',templates.email_single_col_text,[{'label':'Properties','properties':[{ 'label':'HTML Text', 'selector': 'html_text', 'value': '<p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>','is_hint': false,'hint_text':'','is_file':false }]}]));

      widgets.push(new Widget(7, 3,3,"Two Column Layout Text", 1, "icon-text-box-tool", 'EmailTwoColumnTextComponent',templates.email_two_col_text,[{'label':'First Column','properties':[{ 'label':'Heading', 'selector': 'heading_1', 'value': 'Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Text Content', 'selector': 'html_text_1', 'field':'editor', 'value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]},{'label':'Second Column','properties':[{ 'label':'Heading', 'selector': 'heading_2', 'value': 'Heading','is_hint': false,'hint_text':'','is_file':false },{ 'label':'Text Content', 'selector': 'html_text_2', 'field':'editor','value': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','is_hint': false,'hint_text':'','is_file':false }]}]));

      widgets.push(new Widget(8, 3,4, "Two Product Section", 1, "icon-two-side-image", 'EmailTwoProductComponent',templates.email_two_side_banner,[{'label':'First Product', 'properties':[{'label':'Image', 'selector': 'product1_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Product Name', 'selector': 'product1_name', 'value': 'Product 1','is_hint': false,'hint_text':'','is_file':false },{'label':'Product Price', 'selector': 'product1_price', 'value': '$200','is_hint': false,'hint_text':'','is_file':false },{'label':'Old Price', 'selector': 'product1_old_price', 'value': '','is_hint': true,'hint_text':'Put blank if not applicable','is_file':false }]},{'label': 'Second Product', 'properties': [{'label':'Image', 'selector': 'product2_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Product Name', 'selector': 'product2_name', 'value': 'Product 2','is_hint': false,'hint_text':'','is_file':false },{'label':'Product Price', 'selector': 'product2_price', 'value': '$200','is_hint': false,'hint_text':'','is_file':false },{'label':'Old Price', 'selector': 'product2_old_price', 'value': '','is_hint': true,'hint_text':'Put blank if not applicable','is_file':false }]}]));  

      widgets.push(new Widget(9, 3,6, "Separator Section", 1, "icon-two-side-image", 'EmailSeparatorComponent',templates.email_two_side_banner,[{'label':'Properties', 'properties':[{'label':'Width', 'selector': 'height', 'value': '2','is_hint': true,'hint_text':'in px','is_file':false },{'label':'Color code', 'selector': 'colorcode', 'field':'colorpicker', 'value': '#999','is_hint': false,'hint_text':'','is_file':false }]}]));  

      widgets.push(new Widget(10, 3,4, "Four Product Section", 1, "icon-folder", 'EmailFourProductComponent',templates.email_two_side_banner,[{'label':'First Product', 'properties':[{'label':'Image', 'selector': 'product1_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Product Name', 'selector': 'product1_name', 'value': 'Product 1','is_hint': false,'hint_text':'','is_file':false },{'label':'Product Price', 'selector': 'product1_price', 'value': '$200','is_hint': false,'hint_text':'','is_file':false },{'label':'Old Price', 'selector': 'product1_old_price', 'value': '','is_hint': true,'hint_text':'Put blank if not applicable','is_file':false }]},{'label': 'Second Product', 'properties': [{'label':'Image', 'selector': 'product2_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Product Name', 'selector': 'product2_name', 'value': 'Product 2','is_hint': false,'hint_text':'','is_file':false },{'label':'Product Price', 'selector': 'product2_price', 'value': '$200','is_hint': false,'hint_text':'','is_file':false },{'label':'Old Price', 'selector': 'product2_old_price', 'value': '','is_hint': true,'hint_text':'Put blank if not applicable','is_file':false }]},{'label':'Third Product', 'properties':[{'label':'Image', 'selector': 'product3_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Product Name', 'selector': 'product3_name', 'value': 'Product 3','is_hint': false,'hint_text':'','is_file':false },{'label':'Product Price', 'selector': 'product3_price', 'value': '$200','is_hint': false,'hint_text':'','is_file':false },{'label':'Old Price', 'selector': 'product3_old_price', 'value': '','is_hint': true,'hint_text':'Put blank if not applicable','is_file':false }]},{'label':'Fourth Product', 'properties':[{'label':'Image', 'selector': 'product4_img', 'value': this.cdnRootUrl+'/assets/images/img2.jpg','is_hint': false,'hint_text':'','is_file':true, 'type':0,'image_size': { width: 570, height: 330 } },{'label':'Product Name', 'selector': 'product4_name', 'value': 'Product 4','is_hint': false,'hint_text':'','is_file':false },{'label':'Product Price', 'selector': 'product4_price', 'value': '$200','is_hint': false,'hint_text':'','is_file':false },{'label':'Old Price', 'selector': 'product4_old_price', 'value': '','is_hint': true,'hint_text':'Put blank if not applicable','is_file':false }]} ]));      

      widgets.push(new Widget(11, 3,6, "Button", 1, "icon-link-button", 'EmailButtonComponent',templates.email_two_side_banner,[{'label':'Properties', 'properties':[{'label':'Text', 'selector': 'btn_text', 'value': 'Button','is_hint': false,'hint_text':'','is_file':false },{'label':'Text Color', 'selector': 'text_colorcode', 'field':'colorpicker', 'value': '#ffffff','is_hint': false,'hint_text':'','is_file':false },{'label':'Background Color', 'selector': 'bg_colorcode', 'field':'colorpicker', 'value': '#012f84','is_hint': false,'hint_text':'','is_file':false },{'label':'Round Corner', 'selector': 'round_px', 'value': '','is_hint': true,'hint_text':'in px','is_file':false },{'label':'Link', 'selector': 'action_link', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));

      widgets.push(new Widget(12, 3,6, "Two Buttons", 1, "icon-link-button", 'EmailButtonTwoComponent',templates.email_two_side_banner,[{'label':'First Button', 'properties':[{'label':'Text', 'selector': 'btn_text1', 'value': 'Button One','is_hint': false,'hint_text':'','is_file':false },{'label':'Text Color', 'selector': 'text_colorcode1', 'field':'colorpicker', 'value': '#ffffff','is_hint': false,'hint_text':'','is_file':false },{'label':'Background Color', 'selector': 'bg_colorcode1', 'field':'colorpicker', 'value': '#012f84','is_hint': false,'hint_text':'','is_file':false },{'label':'Round Corner', 'selector': 'round_px1', 'value': '','is_hint': true,'hint_text':'in px','is_file':false },{'label':'Link', 'selector': 'action_link1', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]},{'label':'Second Button', 'properties':[{'label':'Text', 'selector': 'btn_text2', 'value': 'Button Two','is_hint': false,'hint_text':'','is_file':false },{'label':'Text Color', 'selector': 'text_colorcode2', 'field':'colorpicker', 'value': '#ffffff','is_hint': false,'hint_text':'','is_file':false },{'label':'Background Color', 'selector': 'bg_colorcode2', 'field':'colorpicker', 'value': '#012f84','is_hint': false,'hint_text':'','is_file':false },{'label':'Round Corner', 'selector': 'round_px2', 'value': '','is_hint': true,'hint_text':'in px','is_file':false },{'label':'Link', 'selector': 'action_link2', 'value': this.rootURI,'is_hint': false,'hint_text':'','is_file':false }]}]));  

      return widgets;
  }


  //This will of course later pull from backend
  getWidgets(cat_id:number,type:number=1 ,website_id:number=1){
    var widgets = [];
    if(type==1) {
      widgets = this.widgetList();
    } else {
       widgets = this.widgetListEmail();
    }
    let return_widgets:any = [];
    widgets.forEach(item=>{
      if(item.widget_category==cat_id){
        if(website_id == 1 && (item.is_distributor==1 || item.is_distributor==3)){
          return_widgets.push(item);
        } else if(website_id > 1 && (item.is_distributor==2 || item.is_distributor==3)){
          return_widgets.push(item);
        }
      }
    });
    return return_widgets;
  }

  getWidgetCategories() {
    let widget_category:any = [
      { id:1, active: false, hover: false },
      { id:2, active: false, hover: false },
      { id:3, active: false, hover: false },
      { id:4, active: false, hover: false },
      { id:5, active: false, hover: false },
      { id:6, active: false, hover: false }
    ];
    return widget_category;
  }

  getWidgetById(widget_id:number,type:number=1) {
    var widgets = [];
    if(type==1){
      widgets = this.widgetList();
    }else{
       widgets = this.widgetListEmail();
    }
    let return_widget:any = {};
    widgets.forEach(item=>{
      if(item.id==widget_id){
        return_widget = Object.assign({},item);
      }
    });
    return return_widget;
  }

  getWidgetTemplate(widget_id:number,type:number=1){
    var widgets = [];
    if(type==1){
      widgets = this.widgetList();
    }else{
       widgets = this.widgetListEmail();
    }
    let widget_template:any = {};
    widgets.forEach(item=>{
      if(item.id==widget_id){
        widget_template = item.htmlTemplate;
      }
    });
    return widget_template; 
  }

  getTemplateImageSizes() {
    var imageSizes = [];
    imageSizes.push({ template_id: 1, widget_id:1, image_size: { width: 1920, height: 630 }  });
    imageSizes.push({ template_id: 1, widget_id:3, image_size: { width: 370, height: 515 }  });
    imageSizes.push({ template_id: 1, widget_id:4, image_size: { width: 570, height: 330 }  });
    imageSizes.push({ template_id: 1, widget_id:11, image_size: { width: 570, height: 330 }  });
    return imageSizes;
  }


  calcAspectRatio(width:number, ratio: number){ //ratio is in respect of width
    let return_height:number = Math.round(width*(1/ratio));
    let return_data: any = {};
    return_data = { width: width, height: return_height };
    return return_data
  }

  pageLoad(data:any){
   
    return this._http.post(GlobalVariable.BASE_API_URL+'page_url_to_id/', data,this._globalService.getHttpOption()).pipe(map(res =>  res.json()),catchError(this.handleError));
  }

  emailTemplateLoad(data:any){
    return this._http.post(GlobalVariable.BASE_API_URL+'tempidtovalue/', data,this._globalService.getHttpOption()).pipe(map(res =>  res.json()),catchError(this.handleError));  
  }

  cmsAddEdit(data:any){
    let userData = this._cookieService.getObject('userData');
    console.log("************* current user data ****************",userData);
    let headers = new Headers({
      'Authorization': 'Token '+userData['auth_token']
      //'Content-Type': 'multipart/form-data'
    });
    let options = new RequestOptions({ headers: headers });
    return this._http.post(GlobalVariable.BASE_BACKEND_API_URL+'add_page_content/', data,options).pipe(map(res =>  res.json()),catchError(this.handleError));
  }

  emailTemplateAddEdit(data:any){
    let userData = this._cookieService.getObject('userData');
    let headers = new Headers({
      'Authorization': 'Token '+userData['auth_token']
      //'Content-Type': 'multipart/form-data'
    });
    let options = new RequestOptions({ headers: headers });
    return this._http.post(GlobalVariable.BASE_BACKEND_API_URL+'template-master/', data,options).pipe(map(res =>  res.json()),catchError(this.handleError));
  }
  // Error handler method
  private handleError(error: Response) { 
    return Observable.throw(error || "Server err"); 
  }
}