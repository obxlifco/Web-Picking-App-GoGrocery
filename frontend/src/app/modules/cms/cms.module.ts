import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule} from '@angular/forms';
import {PipeModule} from '../../global/pipes/pipe.module';
import {MaterialModule} from '../../global/modules/material.module';
import {SharedModule} from '../../global/modules/shared.module';
import { EditWidgetComponent,FormAddEditFieldComponent } from './edit-widget/edit-widget.component';
import { ColorPickerModule } from 'ngx-color-picker';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { WidgetsService} from './widgets.service';
import { AddEditPageComponent,ManagePageComponent,ManageNavigationComponent,AddEditNavigationComponent } from './page-setup/page.setup.component';

import {   
          BannerComponent,
          CarouselComponent,
          InfoboxComponent,
          VFeaturedBoxComponent,
          HFeaturedBoxComponent,
          FeatureProductComponent,
          CategoriesComponent,
          BrandsWidgetComponent,
          ParentCategoriesComponent,
          NewProductComponent,
          BestSellerProductComponent,
          FreeTextComponent,
          TwoColumnTextComponent,
          ThreeColumnTextComponent,
          ImageWithTextComponent,
          TwoSideBannerComponent,
          HeadingTextComponent,
          FormComponent,
          ThreeSideBannerComponent,
          IntroComponent,
          AboutSectionComponent,
          EmailBannerComponent,
          EmailTwoSideBannerComponent,
          EmailHeadingTextComponent,
          EmailImageWithTextComponent,
          PaymentImage,
          EmailImageWithTwoTextComponent,
      	  EmailFreeTextComponent,
      	  EmailTwoColumnTextComponent,
      	  EmailTwoProductComponent,
      	  EmailSeparatorComponent,
      	  EmailFourProductComponent,
      	  AllProductConditionWise,
      	  EmailButtonComponent,
      	  EmailButtonTwoComponent,
      	  BestSellOrDealProduct,
      	  SubscribeNewsLetter,
      	  OurFeature,
      	  CategoryBanner,
      	  PromotionBanner} from './widgets/cms.widgets.component';
import {WidgetDirective} from './widgets/widget.directive';

import { CmsRoutingModule } from './cms-routing.module';


@NgModule({
  declarations: [
  	EditWidgetComponent,
  	FormAddEditFieldComponent,
  	AddEditPageComponent,
  	ManagePageComponent,
  	ManageNavigationComponent,
  	AddEditNavigationComponent,
  	BannerComponent,
  	CarouselComponent,
  	InfoboxComponent,
  	VFeaturedBoxComponent,
  	HFeaturedBoxComponent,
  	FeatureProductComponent,
  	CategoriesComponent,
  	BrandsWidgetComponent,
  	ParentCategoriesComponent,
  	NewProductComponent,
  	BestSellerProductComponent,
  	FreeTextComponent,
  	TwoColumnTextComponent,
  	ThreeColumnTextComponent,
  	ImageWithTextComponent,
  	TwoSideBannerComponent,
  	HeadingTextComponent,
  	FormComponent,
  	ThreeSideBannerComponent,
  	IntroComponent,
  	AboutSectionComponent,
  	EmailBannerComponent,
  	EmailTwoSideBannerComponent,
  	EmailHeadingTextComponent,
  	EmailImageWithTextComponent,
  	PaymentImage,
  	EmailImageWithTwoTextComponent,
  	EmailFreeTextComponent,
  	EmailTwoColumnTextComponent,
  	EmailTwoProductComponent,
  	EmailSeparatorComponent,
  	EmailFourProductComponent,
  	AllProductConditionWise,
  	EmailButtonComponent,
  	EmailButtonTwoComponent,
  	BestSellOrDealProduct,
  	SubscribeNewsLetter,
  	OurFeature,
  	CategoryBanner,
  	PromotionBanner,
    WidgetDirective,
  ],
  imports: [
    CommonModule,
    CmsRoutingModule,
    PipeModule,
    MaterialModule,
    FormsModule,
    SharedModule,
    ColorPickerModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule
  ],
  exports : [
    WidgetDirective

  ],
  entryComponents : [
	    BannerComponent,
      CarouselComponent,
      InfoboxComponent,
      VFeaturedBoxComponent,
      HFeaturedBoxComponent,
      FeatureProductComponent,
      CategoriesComponent,
      BrandsWidgetComponent,
      ParentCategoriesComponent,
      NewProductComponent,
      BestSellerProductComponent,
      FreeTextComponent,
      TwoColumnTextComponent,
      ThreeColumnTextComponent,
      ImageWithTextComponent,
      TwoSideBannerComponent,
      HeadingTextComponent,
      FormComponent,
      ThreeSideBannerComponent,
      IntroComponent,
      AboutSectionComponent,
      EmailBannerComponent,
      EmailTwoSideBannerComponent,
      EmailHeadingTextComponent,
      EmailImageWithTextComponent,
      PaymentImage,
      EmailImageWithTwoTextComponent,
  	  EmailFreeTextComponent,
  	  EmailTwoColumnTextComponent,
  	  EmailTwoProductComponent,
  	  EmailSeparatorComponent,
  	  EmailFourProductComponent,
  	  AllProductConditionWise,
  	  EmailButtonComponent,
  	  EmailButtonTwoComponent,
  	  BestSellOrDealProduct,
  	  SubscribeNewsLetter,
  	  OurFeature,
  	  CategoryBanner,
  	  PromotionBanner,
      AddEditPageComponent,
      ManagePageComponent,
      ManageNavigationComponent,
      AddEditNavigationComponent,

  ]
})
export class CmsModule { }
