/// ANGULAR IMPORTS////
import { NgModule, enableProdMode } from '@angular/core';
import { APP_BASE_HREF } from '@angular/common';
import { BrowserModule, BrowserTransferStateModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpModule, RequestOptions, Jsonp, JsonpModule,Response } from '@angular/http'; 
import { HttpClientModule, HttpClient } from '@angular/common/http'; // required for translate module
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
import { Global } from './global/service/global';
import { AuthGuardEditor,AuthGuard, AuthGuardMerchant } from './global/service/auth-guard.service';
import { ShoppingCartService } from './global/service/app.cart.service';

///PIPES IMPORTS////
/*import { SafeHtmlPipe,SafeStylePipe,SafeScriptPipe,SafeUrlPipe,SafeResourceUrlPipe } from './global/pipes/safe-html.pipe';
import { TruncatePipe } from './global/pipes/truncate.pipe';*/
import { DecimalPipe } from '@angular/common';

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
import { AppModule } from './app.module';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';
import { BrowserCookiesModule } from '@ngx-utils/cookies/browser';
// Static pages  work....
// AoT requires an exported function for factories
export function HttpLoaderFactory(httpClient: HttpClient) {
    return new TranslateHttpLoader(httpClient, "i18n/", ".json"); 
}

@NgModule({
  imports: [
     
    AppRoutingModule,
    OwlModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpModule,
    CKEditorModule,
    ImageCropperModule,
    MaterialModule,
   
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
    BrowserCookiesModule.forRoot(),
    NgSlimScrollModule,
    CmsModule,
    //NgxQRCodeModule,
    //  Staic pages pending work....
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    AppModule,
    BrowserTransferStateModule,
    ServiceWorkerModule.register('ngsw-worker.js', { enabled: environment.production })
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
      Global,
      {
          provide: SLIMSCROLL_DEFAULTS,
          useValue: {
            alwaysVisible : false,
          }
      },            
  ],
  bootstrap: [
    AppComponent
  ],
  entryComponents: [
    ConfirmDialog,
    AlertDialog,    
    ProductDetailSnakbarComponent,
    PopupImgDirective,
    ImageUploadUrlDialog,
    ImageMetaDataDialog,
    ImageUploadLibDialog,
    PopupIconDirective,
    ImageCropDirective
  ],
  exports: [ConfirmDialog,AlertDialog,ImagecropperModule],
})
export class AppBrowserModule { }
