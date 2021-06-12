import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { CookieService,CookieModule } from 'ngx-cookie';
import { RatingModule} from "ngx-rating";
import { DndModule} from 'ng2-dnd';
import { CKEditorModule } from 'ng2-ckeditor';
import { ImageCropperModule} from 'ngx-image-cropper';
import { ColorPickerModule } from 'ngx-color-picker';
import {ImageCropperComponent, CropperSettings, Bounds} from 'ng2-img-cropper';
import { OwlModule } from 'ngx-owl-carousel';


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RatingModule,
    ColorPickerModule,
    DndModule.forRoot(),
    CKEditorModule,
    OwlModule,
  ],
  exports : [
  	RatingModule,
    ColorPickerModule,
    DndModule,
    CKEditorModule,
    OwlModule
  ]
})
export class SharedModule { }
