/// ANGULAR IMPORTS////
import { NgModule, enableProdMode,ErrorHandler} from '@angular/core';
import { APP_BASE_HREF, DatePipe } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule ,ReactiveFormsModule} from '@angular/forms';
import { HttpModule, RequestOptions, Jsonp, JsonpModule,Response } from '@angular/http'; 
import { HttpClientModule, HttpClient } from '@angular/common/http'; // required for translate module
import {HTTP_INTERCEPTORS} from '@angular/common/http';
import {LoaderInterceptor} from './core/intercepter/loader.interceptor';
// Import material module 
import {MaterialModule} from './global/modules/material.module'; 
import 'hammerjs';

////GLOBAL IMPORTS////
import { AppComponent } from './app.component';
import { AppRoutingModule} from './app-routing.module';
import {HeaderComponent} from './ui/header/header.component';
import {FooterComponent} from './ui/footer/footer.component';
import {ProductDetailSnakbarComponent} from './ui/snackbar/app.snackbar.component';
import { GlobalService } from './global/service/app.global.service';
import { CustomErrorHandlerService } from './global/service/customerrorhandaler.service';
import { AuthGuardEditor,AuthGuard, AuthGuardMerchant } from './global/service/auth-guard.service';
import { ShoppingCartService } from './global/service/app.cart.service';

///PIPES IMPORTS////
/*import { SafeHtmlPipe,SafeStylePipe,SafeScriptPipe,SafeUrlPipe,SafeResourceUrlPipe } from './global/pipes/safe-html.pipe';
import { TruncatePipe } from './global/pipes/truncate.pipe';*/
import { DecimalPipe, CommonModule } from '@angular/common';

///DIRECTIVES IMPORTS////

import { EqualValidator, SafeValidator,passwordValidator,MinValidator,MaxValidator } from './global/directives/equal-validator.directive';
import { PopupImgDirective,ImageUploadUrlDialog,ImageMetaDataDialog,ImageUploadLibDialog } from './global/directives/popup-image.directive';
import { PopupIconDirective } from './global/directives/popup-icon.directive';
import { ImageCropDirective } from './global/directives/image-crop.directive';
import { ConfirmDialog,AlertDialog }   from './global/dialog/confirm-dialog.component';
import { DialogsService } from './global/dialog/confirm-dialog.service';

////PLUGIN IMPORTS////
import { CookieService,CookieModule } from 'ngx-cookie';
import { DndModule} from 'ng2-dnd';
import { CKEditorModule } from 'ng2-ckeditor';
import { ImageCropperModule} from 'ngx-image-cropper';
import {ImageCropperComponent, CropperSettings, Bounds} from 'ng2-img-cropper';
// import { ImageZoomModule} from 'angular2-image-zoom';
import { RatingModule} from "ngx-rating";
 import { FacebookModule } from 'ngx-facebook';
import { ColorPickerModule } from 'ngx-color-picker';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';

import { TranslateModule, TranslateLoader,TranslateService } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { NgSlimScrollModule, SLIMSCROLL_DEFAULTS } from 'ngx-slimscroll';
import {CmsModule} from './modules/cms/cms.module';
/*import {WidgetDirective} from './cms/widgets/widget.directive';*/
/*import {ViewOrdersComponent} from './profile/app.profile.component';*/

//caraosal import
import { OwlModule } from 'ngx-owl-carousel';
import { ImagecropperModule } from './global/modules/imagecropper/imagecropper.module';
/*import { ImagetransformPipe } from './global/pipes/imagetransform.pipe';*/
import { UiComponent } from './ui/ui.component';
import { TransferHttpCacheModule } from '@nguniversal/common';
import { NgtUniversalModule } from '@ng-toolkit/universal';
import { LoaderComponent } from './global/component/loader/loader.component';
import { WarehouselistComponent } from './global/dialog/warehouselist/warehouselist.component';
import { LocationdialogComponent } from './global/dialog/locationdialog/locationdialog.component';
import { FinetuninglocationComponent } from './global/dialog/finetuninglocation/finetuninglocation.component';
/*import { AgmCoreModule } from '@agm/core';*/
import { NowarehousefoundComponent } from './global/dialog/nowarehousefound/nowarehousefound.component';
import { storecategorylistComponent } from './global/dialog/storecategorylist/storecategorylist.component';

import {PipeModule} from './global/pipes/pipe.module';

import { LoginComponent } from './login/login.component';

// Static pages  work....
// AoT requires an exported function for factories
export function HttpLoaderFactory(httpClient: HttpClient) {
    return new TranslateHttpLoader(httpClient, "i18n/", ".json"); 
}
  // social login

import { SocialLoginModule, AuthServiceConfig } from "angularx-social-login";
import { GoogleLoginProvider, FacebookLoginProvider } from "angularx-social-login";
import { SignUpComponent } from './modules/sign-up/sign-up.component';
import { ForgetPasswordComponent } from './forget-password/forget-password.component';
import { SkeltonComponent } from './global/component/skelton/skelton.component';
import { HeaderOnlyLogoComponent } from './ui/header-only-logo/header-only-logo.component';
import { SuccesspaymentComponent } from './modules/successpayment/successpayment.component';
import { FailepaymentComponent } from './modules/failepayment/failepayment.component';
import { CancelpaymentComponent } from './modules/cancelpayment/cancelpayment.component';
import { ContactusComponent } from './contactus/contactus.component';
import { MobileLandingComponent } from './mobile-landing/mobilelanding.component';
import { PromotionComponent } from './promotion/promotion.component';
import { SuccessSubstituteComponent } from './modules/substitute_product/successSubstituteProduct/successSubstitute.component';
import { SelectOptionComponent } from './global/dialog/selectoption/selectoption.component';
import { CartoptionpopupComponent } from './global/dialog/cartoptionpopup/cartoptionpopup.component';
import { SubstitutioncartoptionComponent } from './global/dialog/substitutioncartoption/substitutioncartoption.component';
let config = new AuthServiceConfig([
  {
    id: GoogleLoginProvider.PROVIDER_ID,
    //provider: new GoogleLoginProvider("603575321949-ftns9e47ki8lq1kfs6onss6842lh28u0.apps.googleusercontent.com")
    provider: new GoogleLoginProvider("104850538263-rs1i4rki7h9i3snp99vat13v2h0gt2ii.apps.googleusercontent.com")

  },
  {
    id: FacebookLoginProvider.PROVIDER_ID,
    provider: new FacebookLoginProvider("269932210679127")
  }
]);
 
export function provideConfig() {
  return config;
}
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    ProductDetailSnakbarComponent,
    ConfirmDialog,
    AlertDialog,
    PopupImgDirective,
    ImageUploadUrlDialog,
    ImageMetaDataDialog,
    ImageUploadLibDialog,
    PopupIconDirective,
    ImageCropDirective, 
    EqualValidator,
    SafeValidator,
    passwordValidator,
    MinValidator,
    MaxValidator,
    UiComponent,
    LoaderComponent,
    WarehouselistComponent,
    LocationdialogComponent,
    FinetuninglocationComponent,
    NowarehousefoundComponent,
    SelectOptionComponent,
    storecategorylistComponent,
    LoginComponent,
    SignUpComponent,
    ForgetPasswordComponent,
    SkeltonComponent,
    HeaderOnlyLogoComponent,
    SuccesspaymentComponent,
    FailepaymentComponent,
    CancelpaymentComponent,
    ContactusComponent,
    MobileLandingComponent,
    PromotionComponent,
    SuccessSubstituteComponent,
    CartoptionpopupComponent,
    SubstitutioncartoptionComponent
  ],
  imports: [
    SocialLoginModule,
    BrowserModule.withServerTransition({ appId: 'serverApp' }), 
    AppRoutingModule,
    OwlModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    CKEditorModule,
    ImageCropperModule,
    MaterialModule,
    PipeModule,
   
    // ImageZoomModule,
    RatingModule,
    ColorPickerModule,
    DndModule.forRoot(),
    CookieModule.forRoot(),
    FacebookModule.forRoot(),
    HttpClientModule,
    TranslateModule.forRoot({
        loader: {
          provide: TranslateLoader,
          useFactory: HttpLoaderFactory,
          deps: [HttpClient]
        }
    }),
   /* AgmCoreModule.forRoot({
      apiKey: 'AIzaSyDwJfFz9Hyur4RkbEa_Hlt6Fkibr6rYhJo',
      libraries: ['places','geocode','maps']
    }),*/
    NgSlimScrollModule,
    CmsModule,
    //NgxQRCodeModule,
    //  Staic pages pending work....
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    CommonModule,
    TransferHttpCacheModule,
    NgtUniversalModule
  ],
  providers: [ 
      GlobalService,
      CookieService,
      AuthGuardEditor,
      AuthGuard,
      AuthGuardMerchant,
      DialogsService,
      ShoppingCartService,
      DecimalPipe,
      DatePipe,
      {
        provide: AuthServiceConfig,
        useFactory: provideConfig
      },
      {
          provide: SLIMSCROLL_DEFAULTS,
          useValue: {
            alwaysVisible : false,
          }
      },
      { provide: HTTP_INTERCEPTORS, useClass: LoaderInterceptor, multi: true },
      /*{
        provide: ErrorHandler, useClass:CustomErrorHandlerService
      }  */        
  ],
  bootstrap: [
    AppComponent
  ],
  entryComponents: [
    ConfirmDialog,
    AlertDialog,
    LoginComponent,
    SignUpComponent,
    ForgetPasswordComponent,
    ProductDetailSnakbarComponent,
    PopupImgDirective,
    ImageUploadUrlDialog,
    ImageMetaDataDialog,
    ImageUploadLibDialog,
    PopupIconDirective,
    ImageCropDirective,
    WarehouselistComponent,
    LocationdialogComponent,
    FinetuninglocationComponent,
    NowarehousefoundComponent,
    storecategorylistComponent,
    SelectOptionComponent,
    CartoptionpopupComponent,
    SubstitutioncartoptionComponent
    ],
  exports: [ConfirmDialog,AlertDialog,ImagecropperModule],
})
export class AppModule { }
