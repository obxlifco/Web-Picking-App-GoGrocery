import { Component,Inject, OnInit,ViewChild,AfterViewInit} from '@angular/core';
import { DOCUMENT} from '@angular/platform-browser';
import { MatDialogRef,MatDialog,MAT_DIALOG_DATA } from '@angular/material';
import { GlobalService } from '../service/app.global.service';
import { Global,GlobalVariable } from '.././service/global';
/*import {ImageCropperComponent,ImageCroppedEvent} from 'ngx-image-cropper';*/
//import {ImageCropperComponent, CropperSettings, Bounds} from 'ng2-img-cropper';
/*import {ImageCropperComponent,CropperSettings,Bounds} from 'ng2-img-cropper';
import {ImagecropperModule} from '../modules/imagecropper/imagecropper.module';*/

import { ImageCroppedEvent,ImageCropperComponent} from 'ngx-image-cropper';


// https://www.npmjs.com/package/ngx-image-cropper by cds ref

@Component({
  selector: 'image-crop-dialog',
  templateUrl: 'image-crop-dialog.html',
  providers: [Global],
})
export class ImageCropDirective implements OnInit,AfterViewInit{
    imageChangedEvent: any = '';
    croppedImage: any = '';
    public crop_data:any = {};
    public data_content:any ={};
    public file_name:any = '';
    /*public cropperSettings:CropperSettings;
    public crop_data:any;
    public data_content:any ={};
*/
   @ViewChild('cropper', undefined) cropper:ImageCropperComponent;

    constructor(
                public _global: Global,
                public _globalService: GlobalService,
                public dialogRef: MatDialogRef<ImageCropDirective> ,
                public dialog: MatDialog,
                @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
        /*this.cropperSettings = new CropperSettings();
        this.cropperSettings.noFileInput = true;
        this.cropperSettings.width = this.data.image_size.width;
        this.cropperSettings.height = this.data.image_size.height;

        this.cropperSettings.croppedWidth = this.data.image_size.width;
        this.cropperSettings.croppedHeight = this.data.image_size.height;

        this.cropperSettings.canvasWidth = this.data.canvas_size.width;
        this.cropperSettings.canvasHeight = this.data.canvas_size.height;

        this.cropperSettings.minWidth = this.data.image_size.width;
        this.cropperSettings.minHeight = this.data.image_size.height;

        this.cropperSettings.rounded = false;
        this.cropperSettings.keepAspect = true;

        this.cropperSettings.cropperDrawSettings.strokeColor = 'rgba(2,148,215,1)';
        this.cropperSettings.cropperDrawSettings.strokeWidth = 2;
        this.cropperSettings.preserveSize = false;

        this.cropperSettings.dynamicSizing = false;

        this.crop_data = {};*/


    } 

   

   /* cropped(bounds:Bounds) {
        this.crop_data['crop_data'] = {};
        this.crop_data['crop_data']['image_x1'] = bounds.top;
        this.crop_data['crop_data']['image_y1'] = bounds.left;
        this.crop_data['crop_data']['image_x2'] = bounds.right;
        this.crop_data['crop_data']['image_y2'] = bounds.bottom;
        this.crop_data['crop_data']['image_width'] = bounds.width;
        this.crop_data['crop_data']['image_height'] = bounds.height;
        this.crop_data['crop_data']['dir_name'] = this.data.dir_name;
        this.crop_data['_file'] = this.data['_file'];
      
    }*/
     ngOnInit(){
       
        this.data_content['img'] = this.data.url;
        this.data_content['aspect_ratio'] = this.data.aspect_ratio;
        this.data_content['converted_img_width'] = this.data.image_size.width;
        this.data_content['converted_img_height'] =  this.data.image_size.height;
        this.data_content['img_width']  = this.data['ori_img_size']['width'];
        this.data_content['img_height'] = this.data['ori_img_size']['height'];
        this.data_content['file_name'] = this.data['_file']['name'];
        if(this.data['file_change_event']) {
            this.fileChangeEvent(this.data['file_change_event']);
        }

       
    }
    ngAfterViewInit() {
        let image:HTMLImageElement = new Image();
        image.src= this.data.url;
    }
    fileChangeEvent(event: any): void {

        this.imageChangedEvent = event;
    }
    imageCropped(event: ImageCroppedEvent) {
        this.crop_data['crop_data'] = {};
        this.crop_data['crop_data']['image_x1'] = event.cropperPosition.x1;
        this.crop_data['crop_data']['image_y1'] = event.cropperPosition.y1;
        this.crop_data['crop_data']['image_x2'] = event.cropperPosition.x2;
        this.crop_data['crop_data']['image_y2'] = event.cropperPosition.y2;
        this.crop_data['crop_data']['image_width'] = event.width;
        this.crop_data['crop_data']['image_height'] = event.height;
        this.crop_data['crop_data']['dir_name'] = this.data.dir_name;
        let fileName = 'imageupload.png';
        this.crop_data['crop_data']['_file'] = new File([event.file],fileName);
        
        this.croppedImage = event.base64;
    }
    imageLoaded() {
        // show cropper
    }
    cropperReady() {
        // cropper ready
    }
    loadImageFailed() {
        // show message
    }
    

    saveCrop(){

        var form_data = new FormData();
        //console.log(this.)
        form_data.append('image_data', JSON.stringify(this.crop_data['crop_data']));
        form_data.append('file', this.crop_data['crop_data']['_file']);
        this._global.uploadCroppedImage(form_data).subscribe(
            data => {
              if(data.status){

                    let return_data = {media_dir: data.media_dir, dir_name: data.dir_name};
                    this.dialogRef.close(return_data);    
                }
                
            }
        );     
        
    }
    

    closeDialog(){
        this.dialogRef.close();
    }         
}