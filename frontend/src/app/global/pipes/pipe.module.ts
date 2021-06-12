import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { SafeHtmlPipe,SafeStylePipe,SafeScriptPipe,SafeUrlPipe,SafeResourceUrlPipe} from './safe-html.pipe';
import { ImagetransformPipe } from '../../global/pipes/imagetransform.pipe';
import {TruncatePipe} from './truncate.pipe';
import {DecimalPipe} from '@angular/common';
import { TranslateModule, TranslateLoader,TranslateService } from '@ngx-translate/core';
import {MatIconModule} from '@angular/material/icon';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { MoneyPipe } from './money.pipe';
import { CartcountPipe } from './cartcount.pipe';
export function HttpLoaderFactory(httpClient: HttpClient) {
    return new TranslateHttpLoader(httpClient, "i18n/", ".json"); 
}

@NgModule({
  declarations: [
  	SafeHtmlPipe,
    ImagetransformPipe,
  	SafeStylePipe,
  	SafeScriptPipe,
  	SafeUrlPipe,
  	TruncatePipe,
  	SafeResourceUrlPipe,
  	MoneyPipe,
  	CartcountPipe
  ],
  imports: [
    CommonModule,
    TranslateModule.forRoot({
        loader: {
          provide: TranslateLoader,
          useFactory: HttpLoaderFactory,
          deps: [HttpClient]
        }
    }),
    MatIconModule,
  ],
  exports : [
  	SafeHtmlPipe,
    MoneyPipe,
  	SafeStylePipe,
    ImagetransformPipe,
  	SafeScriptPipe,
  	SafeUrlPipe,
  	TruncatePipe,
  	SafeResourceUrlPipe,
    TranslateModule,
    MatIconModule
  ]
})
export class PipeModule { }