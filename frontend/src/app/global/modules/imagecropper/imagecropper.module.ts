import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageCropperModule } from 'ngx-image-cropper';
@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    ImageCropperModule
  ],
  exports : [
  	ImageCropperModule
  ],
})
export class ImagecropperModule { }
