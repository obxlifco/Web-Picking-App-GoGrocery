import { Component,Inject, OnInit } from '@angular/core';
import { DOCUMENT } from '@angular/platform-browser';
import { MatDialogRef,MatDialog,MAT_DIALOG_DATA } from '@angular/material';
import { GlobalService } from '../service/app.global.service';
import { Global,GlobalVariable } from '.././service/global';
// Google Drive setup
declare const gapi: any;
declare var google; 
// The Browser API key obtained from the Google API Console.
var developerKey = 'AIzaSyD89drcF2t467d219n3mNHaiHyEGD_u1ko';
// The Client ID obtained from the Google API Console. Replace with your own Client ID.
var clientId = "74854632065-86uci4hndsgo2eljc8nh45uh2ol2qgtg.apps.googleusercontent.com"
// Scope to use to access user's photos.
var scope = ['https://www.googleapis.com/auth/drive.readonly'];
var pickerApiLoaded = false;
var oauthToken;
// dropbox setup
declare const Dropbox: any;
@Component({
    selector: 'image-pop',
    templateUrl: './image-pop.html'
})
export class PopupImgDirective {
    constructor(
        public dialogRefPop: MatDialogRef<PopupImgDirective> ,
        public dialog: MatDialog,
        @Inject(MAT_DIALOG_DATA) public data: any,
        public _globalService:GlobalService,
        @Inject(DOCUMENT) private document: any
    ) {
        dialog.afterOpen.subscribe(() => {
        //    let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
        //    containerElem.classList.add('pop-box-up');
        });
    }

    fileChoose(e: Event){
        var files: any = [];
        var target: HTMLInputElement = e.target as HTMLInputElement;
        var file_arr: any = [];
        for(var i=0;i < target.files.length; i++) {
            if(this.check_file_ext(target.files[i].type)){
                if(target.files[i].size < 2097152) {
                    let temp_arr = [];
                    var reader = new FileReader();
                    reader.readAsDataURL(target.files[i]);
                    reader.onload = (event) => {
                        temp_arr['url'] = event.srcElement['result']
                    }
                    temp_arr['_file'] = target.files[i];
                    file_arr.push(temp_arr);
                    let myelement: HTMLElement = this.document.getElementsByClassName('autoclickImage');
                } else {
                    this._globalService.showToast('The image must be less than 2MB.');
                }
            } else {
                this._globalService.showToast('Only jpeg/png/gif files are allowed');
            }
        }
        files[this.data.imgFor] = file_arr;
        // let myelement: HTMLElement = this.document.getElementsByClassName('autoclickImage');
        // myelement[0].click();
        this.dialogRefPop.close(files);
        let myelementnew: HTMLElement = this.document.getElementsByClassName('autoclickImage');
        myelementnew[0].click();
    }

    dialogImgUrlRef: MatDialogRef<ImageUploadUrlDialog> | null;
    openLinkbox(){
        this.dialogRefPop.close();
        this.dialogImgUrlRef = this.dialog.open(ImageUploadUrlDialog,{data: this.data.imgFor});
        this.dialogImgUrlRef.afterClosed().subscribe(result => {
            this._globalService.imageArraySource.next(result);
        });
    }

    // image libray s3
    dialogImgLibRef: MatDialogRef<ImageUploadLibDialog> | null;
    uploadFromLibrary() {
        this.dialogRefPop.close();
        this.dialogImgLibRef = this.dialog.open(ImageUploadLibDialog,{data: this.data});
        this.dialogImgLibRef.afterClosed().subscribe(result => {
            this._globalService.libArraySource.next(result);
        });
    }

    // Use the API Loader script to load google.picker and gapi.auth.
     uploadFromDrive() {
        this.dialogRefPop.close();
        gapi.load('auth', {'callback': this.onAuthApiLoad.bind(this)});
        gapi.load('picker', {'callback': this.onPickerApiLoad.bind(this)});
    }

    onAuthApiLoad() {
        let self = this;
        gapi.auth.authorize(
            {
              'client_id': clientId,
              'scope': scope,
              'immediate': false
            },
            self.handleAuthResult.bind(self));
    }

    onPickerApiLoad() {
        pickerApiLoaded = true;
        //this.createPicker();
    }

    public handleAuthResult(authResult) {
        let self = this;
        if (authResult && !authResult.error) {
          oauthToken = authResult.access_token;
          self.createPicker();
        }
    }

    // Create and render a Picker object for picking user Photos.
    public createPicker() {
        if (pickerApiLoaded && oauthToken) {
            var picker = new google.picker.PickerBuilder().
                addView(google.picker.​ViewId.DOCS_IMAGES).
                setOAuthToken(oauthToken).
                //setDeveloperKey(developerKey).
                setCallback(this.pickerCallback.bind(this)).
                build();
            picker.setVisible(true);

        }
    }

    // A simple callback implementation.
    pickerCallback(data) {
        var imageID = '';
        var url = '';
        if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
            var doc = data[google.picker.Response.DOCUMENTS][0];
            imageID = doc[google.picker.Document.ID];
            url = 'https://docs.google.com/uc?export=view&id='+imageID // this is direct download link
            //url = doc[google.picker.Document.URL];
            var files: any = {};
            var file_arr: any = [];
            file_arr['url'] = url;
            files[this.data.imgFor] = file_arr;
            this._globalService.imageArraySource.next(files);
        }
    }

    onDropboxLoad(){
        let that = this;
        // dropbox options
        var options = {
            // Required. Called when a user selects an item in the Chooser.
            success: function(files) {
                that.onDropboxSucc(files);
            },
            // Optional. Called when the user closes the dialog without selecting a file
            // and does not include any parameters.
            cancel: function() {
            },
            // Optional. "preview" (default) is a preview link to the document for sharing,
            // "direct" is an expiring link to download the contents of the file. For more
            // information about link types, see Link types below.
            linkType: "direct",
            // Optional. A value of false (default) limits selection to a single file, while
            // true enables multiple file selection.
            multiselect: false, // or true
            // Optional. This is a list of file extensions. If specified, the user will
            // only be able to select files with these extensions. You may also specify
            // file types, such as "video" or "images" in the list. For more information,
            // see File types below. By default, all extensions are allowed.
            extensions: ['.jpg', '.jpeg', '.png'],
        }
        Dropbox.choose(options);
    }

    onDropboxSucc(files){
        var url = '';
        url = files[0].link;
        var files: any = {};
        var file_arr: any = [];
        file_arr['url'] = url;
        files[this.data.imgFor] = file_arr;
        this._globalService.imageArraySource.next(files);
        this.dialogRefPop.close();
    }

    check_file_ext(type: string){
        var return_result = 0;
        switch (type) {
            case "image/png":
                return_result= 1;
                break;
            case "image/gif":
                return_result= 1;
                break;
            case "image/jpeg":
                return_result= 1;
                break;
            default:
                return_result= 0;
                break;
        }
        return return_result;
    }
}

@Component({
  selector: 'dialog-image-upload-url',
  templateUrl: 'image-upload-url-dialog.html',
})
export class ImageUploadUrlDialog {
    constructor(
        public dialogRefPop: MatDialogRef<ImageUploadUrlDialog> ,
        public dialog: MatDialog,
        @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
    } 

    insertLink(formVal){
        var files: any = {};
        var file_arr: any = [];
        file_arr['url'] = formVal.imgLink;
        files[this.data] = file_arr;
        this.dialogRefPop.close(files);
    }
}

@Component({
  selector: 'dialog-image-meta-data',
  templateUrl: 'image-meta-data-dialog.html',
})
export class ImageMetaDataDialog {
    public formModel: any = {};
    constructor(
        public dialogRefPop: MatDialogRef<ImageMetaDataDialog> ,
        public dialog: MatDialog,
    @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
        });
        if(data['meta']){
            this.formModel = data['meta'];
        }
    }

    insertMetaData(formVal){
        let meta_content = formVal;
        if(this.data['meta']){
            meta_content['id'] = this.data['meta']['id'];
        }
        meta_content['type'] = this.data['type'];
        meta_content['index'] = this.data['index'];
        meta_content['is_cover'] = this.data['is_cover'];
        this.dialogRefPop.close(meta_content);
    }
}

@Component({
  selector: 'image-lib-dialog',
  templateUrl: 'image-lib-dialog.html',
  providers: [Global]
})
export class ImageUploadLibDialog implements OnInit {
    public images: any = [];
    public s3_link: string;
    constructor(
        public _global: Global,
        public dialogRefPop: MatDialogRef<ImageUploadLibDialog> ,
        public dialog: MatDialog,
        @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        });
        this.s3_link = GlobalVariable.S3_URL+this.data.type+'/200x200/';
    } 

    ngOnInit(){
        this.images=[];
        let that = this;
        this._global.libLoad(this.data.type).subscribe(
            data => {
                if(this.data.type=='category'){
                    if(this.data.imgFor=='banner_image') {
                       data.category_banner_image.forEach(function(item:any){
                          that.images.push({'name': item, 'selected': false });
                        });   
                    } else if(this.data.imgFor=='image') {
                       data.category_images.forEach(function(item:any){
                         that.images.push({'name': item, 'selected': false });
                        }); 
                    } else {
                      this.s3_link = GlobalVariable.S3_URL+this.data.type+'/100x100/';  
                          data.category_thumb_image.forEach(function(item:any){
                            that.images.push({'name': item, 'selected': false });
                           });  
                    }
                } else {
                    data.images.forEach(function(item:any){
                        that.images.push({'name': item, 'selected': false });
                    });
                }
                that.images.filter(function(value, index){ return that.images.indexOf(value) == index });
            },
            err => console.log(err),
            function(){
                //completed callback
            }
        );
    }
    selectImg(index: number){
        if(this.data.is_multiple){
            this.images[index].selected = !this.images[index].selected;
        } else {
            this.images.forEach(function(item:any, idx: number){
                if(index == idx){
                    item.selected = true;
                }else{
                    item.selected = false;
                }
            });
        }
    }
    saveSelectedImage(){
        var files: any = {};
        var file_arr: any = [];
        this.images.forEach(function(item:any){
            if(item.selected){
                file_arr.push({'url': item.name});
            }
        });  
        files[this.data.imgFor] = file_arr;
        this.dialogRefPop.close(files);
    }
    closeDialog(){
        this.dialogRefPop.close();
    }
}