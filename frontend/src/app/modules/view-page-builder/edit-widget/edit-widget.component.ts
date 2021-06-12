import { Component, OnInit, Input, Output, EventEmitter,ViewChild,AfterViewInit,Inject, PLATFORM_ID } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import { CookieService } from 'ngx-cookie';
import {Widget} from '../../../global/widget/widget';
import { WidgetsService } from '../../../global/widget/widgets.service';
import { PopupImgDirective,ImageUploadUrlDialog } from '../../../global/directives/popup-image.directive';
import { PopupIconDirective } from '../../../global/directives/popup-icon.directive';
import { ImageCropDirective } from '../../../global/directives/image-crop.directive';
import { GlobalService } from '../../../global/service/app.global.service';
import {GlobalVariable } from '../../../global/service/global';
import { PageSetupService } from '../page-setup/page.setup.service';
import {defaultObject} from './default_object';


// dropbox setup
declare const Dropbox: any;
declare var CKEDITOR: any;

@Component({
  selector: 'app-edit-widget',
  templateUrl: './edit-widget.component.html',
  providers: [PageSetupService]
})
export class EditWidgetComponent implements OnInit {
  
  public widget:Widget;
  public widgetIndex:number;
  public template_image_sizes:any = [];
  public template_id:number = 1;
  public widget_image_size:any = {};
  public temp_dir:string = '';
  public page_list: any;
  public editor_config:any = {};
  public addedMoreItem = false;

  @Output() deleteWidget = new EventEmitter();
  @Output() closeWidget = new EventEmitter();
  @Output() updateWidget = new EventEmitter();
  @Input() data: any;

  constructor(
            private domSanitizer: DomSanitizer, 
            public dialog: MatDialog,
            public _globalService:GlobalService,
            public _widgetsService:WidgetsService,
            public _cookieService:CookieService,
            public _pageSetupService:PageSetupService) { 


          this.editor_config = {uiColor: '#ffffff',
                        toolbar: [
                                    { name: 'basicstyles', items: [ 'Maximize','TextColor', 'BGColor', 'Bold', 'Italic', 'Underline'] }
                                ]         
                    };


  }

  ngOnInit() {

    this.widget = this.data.widget;
    console.log("***************** Widget data ***************");
    console.log(this.widget);
    
    this.addedMoreItem = this.widget['type'] == 4 && this.widget['insertables'][0].hasOwnProperty('add_more') ? this.widget['insertables'][0]['add_more'] : false;
    
    this.widgetIndex = this.data.widgetIndex;


      this.template_image_sizes = this._widgetsService.getTemplateImageSizes();
    
      this.template_image_sizes.forEach(item=>{
        if(item.template_id==this.template_id && item.widget_id==this.widget.id){
          this.widget_image_size = item.image_size;
        }
      });
  
      // get aspect ratio of widget image size
      let aspect_ratio: number = +((this.widget_image_size.width / this.widget_image_size.height).toFixed(2));
      
      this.getAllPages();
     
       setTimeout(() => {          
           
              for (var i = 0; i < this.widget.insertables.length; i++) {
  
                for (var j = 0; j < this.widget.insertables[i].properties.length; j++) {
  
                  if(this.widget.insertables[i].properties[j].field == 'editor'){
                    CKEDITOR.disableAutoInline = true;
                    CKEDITOR.inline( 'inline-editor$'+this.widget.insertables[i].properties[j].selector, this.editor_config );      
                    CKEDITOR.instances[ 'inline-editor$'+this.widget.insertables[i].properties[j].selector ].on('blur', (evt) => { 
                      let editor_name = (evt.editor.name);
                      let editor_content = CKEDITOR.instances[editor_name].getData();
                      editor_name = editor_name.split('$');
  
                      this.widget.insertables.forEach(item=>{
                        item.properties.forEach(inneritem=>{
                           if(inneritem.selector == editor_name[1]){
                            inneritem.value = editor_content;
                            this.modelChange();       
                           }
                        });  
                      });
                      
                      
                    });   
                  }
                  
                }
              }      
              
            }); 
  }

  changeEvnt(data:any){
    
    this.widget = data.widget;
    this.widgetIndex = data.widgetIndex;
  }  
  deleteinsertablewiget(deletewiget){
		var index = this.widget['insertables'][0]['properties'].indexOf(deletewiget);
		if (index > -1) {
			this.widget['insertables'][0]['properties'].splice(index, 1);
		 }
	}
  delete(){
    // delete this.widget;
    this.deleteWidget.emit(this.widgetIndex);
  }

  close(){
    this.closeWidget.emit();
    
    for (var i = 0; i < this.widget.insertables.length; i++) {

      for (var j = 0; j < this.widget.insertables[i].properties.length; j++) {

        if(this.widget.insertables[i].properties[j].field == 'editor'){
          let editor_content = CKEDITOR.instances['inline-editor$'+this.widget.insertables[i].properties[j].selector].getData();
          this.widget.insertables[i].properties[j].value = editor_content;
          this.modelChange();       
          CKEDITOR.instances['inline-editor$'+this.widget.insertables[i].properties[j].selector].destroy(true);                 
        }
        
      }
    }      
    
  }

  modelChange(){
  
    this.updateWidget.emit(this.data);
  }

  deleteField(index:number){

    this.widget.insertables[0].fields.splice(index,1);
    this.updateWidget.emit(this.data);
  }

  getAllPages(){
    this._pageSetupService.getAllPages().subscribe(
        data => {
            if(data.status){
              this.page_list = data.api_status;
            }
        },
        err => {
         this._globalService.showToast('Something went wrong. Please try again.');
        },
        function(){
            //completed callback
        }
    );
  }
  /**
   * Method for adding a item
   * @access public
  */
  addNewItem() {
    let defaultObjectKey = this.widget['type'] == 4 && this.widget['insertables'][0].hasOwnProperty('default_object') ? this.widget['insertables'][0]['default_object'] : false;
    if(defaultObjectKey) {
      //{[defaultAdObject]}.value
      this.widget['insertables'][0]['properties'].push(defaultObject[defaultObjectKey]);
    }
    



  }


  dialogRef: MatDialogRef<FormAddEditFieldComponent> | null;
  addField(type:string='add',index:number=0){

    let data: any = {type: type, field_data: {}};
    if(type=='edit'){
      data.field_data = this.widget.insertables[0].fields[index];
    }
    this.dialogRef = this.dialog.open(FormAddEditFieldComponent,{data: data});
    this.dialogRef.afterClosed().subscribe(result => {

      if(result){
        if(type=='add'){
          this.widget.insertables[0].fields.push(result);  
        }else{
          this.widget.insertables[0].fields[index] = result;
        }
        
        this.modelChange();  
      }
      
    });
  }


  dialogRefImg: MatDialogRef<PopupImgDirective> | null;
  openImagePop(imgFor: string, multiple: boolean = false){

      let data = { imgFor: imgFor, is_multiple: multiple, type: 'product' };
      
      this.dialogRefImg = this.dialog.open(PopupImgDirective,{data: data});
      this.dialogRefImg.afterClosed().subscribe(result => {
        for (let key in result) {
            let value = result[key][0];
            value['type'] = 2; // image upload type - 2 i.e upload from browse file
            this.widget.insertables[0]['properties'].forEach(item=>{
              if(item.selector==key){
                item.value = value.url;
                item.type = value.type;                
              }
            });
        }
        this.modelChange();
      });

      this._globalService.imageArrayChange$.subscribe(result => {
        
          for (let key in result) {
            let value = result[key];
            value['type'] = 1;  // image upload type - 1 i.e upload from inserted link,google picker, dropbox picker

            this.widget.insertables.forEach(item=>{
              if(item.selector==key){
                item.value = value.url;
                item.type = value.type;

              }
            });

          }
          this.modelChange();
      });

     this._globalService.libArrayChange$.subscribe(result => {
      
        for (let key in result) {
          let value = result[key][0];
          value['type'] = 3;  // image upload type - 3 i.e upload from s3 library
          this.widget.insertables.forEach(item=>{
            if(item.selector==key){
              item.value = GlobalVariable.S3_URL+'product/200x200/'+value['url'];
              item.type = value.type;

            }
          });
         
        }
        this.modelChange();
    });
    
    
  }


    convertToDataURLviaCanvas(url, outputFormat){
      return new Promise( (resolve, reject) => {
        let img = new Image();
        img.crossOrigin = 'Anonymous';
        img.onload = function(){
          let canvas = <HTMLCanvasElement> document.createElement('CANVAS'),
          ctx = canvas.getContext('2d'),
          dataURL;
          canvas.height = img.height;
          canvas.width = img.width;
          ctx.drawImage(img, 0, 0);
          dataURL = canvas.toDataURL(outputFormat);
          //callback(dataURL);
          canvas = null;
          resolve(dataURL); 
        };
        img.src = url;
      });
    }


    dialogRefIcon: MatDialogRef<PopupIconDirective> | null;
    selectIcon(icon:string,selector:string){

      let data = { selected_icon: icon };
      
      this.dialogRefIcon = this.dialog.open(PopupIconDirective,{data: data});
      this.dialogRefIcon.afterClosed().subscribe(result => {
        if(result){
          
          this.widget.insertables.forEach(block=>{
          
            block.properties.forEach(item=>{
              if(item.selector==selector){
                item.value = result;
              }
            });
              
          }); 
          this.modelChange();       
        }
        
      });
    }

    dialogRefImgCrop: MatDialogRef<ImageCropDirective> | null;

    fileChoose(e: Event, imgFor: string, block_index:number){

      let temp_index=block_index;
      if(this.widget.type == 4) {
        block_index =0;
      }
      var files: any = {};
      var target: HTMLInputElement = e.target as HTMLInputElement;

      if(target.files.length>0){
        if(!this._globalService.check_file_ext(target.files[0].type)){
            this._globalService.showToast('Only jpeg/png/gif files are allowed');
        }else if(!this._globalService.check_file_size(target.files[0].size)){
            this._globalService.showToast('Maximum 2MB of file size is allowed');
        }else{
            let temp_arr = {};
            var reader = new FileReader();
            reader.readAsDataURL(target.files[0]);
            reader.onload = (event) => {
                
                var img = new Image;
                var canvas_size = {};
                var ori_img_size = {};

                let srcElm = event.target || event.srcElement; 
                img.onload = () => {
                    

                    var aspect_ratio = +((img.height/img.width).toFixed(2));
                    canvas_size = { width:500, height: 500*aspect_ratio };
                    ori_img_size = {width: img.width, height: img.height};

                    temp_arr['url'] = srcElm['result'];
                    temp_arr['_file'] = target.files[0];
                    temp_arr['type'] = 2; // image upload type - 2 i.e upload from browse file

                    temp_arr['image_size'] = this.widget.insertables[block_index].properties[temp_index].image_size
                    // this.widget.insertables[block_index].properties.forEach(item=>{
                    //   if(item.selector==imgFor){
                    //     temp_arr['image_size'] = item.image_size;
                    //   }
                    // });
                    this.temp_dir = this._globalService.getCookie('temp_dir');
                    if(!this.temp_dir) this.temp_dir = '';
                    let data:any = { dir_name: this.temp_dir,url: temp_arr['url'], image_size: temp_arr['image_size'], canvas_size: canvas_size, _file: temp_arr['_file'], ori_img_size: ori_img_size,aspect_ratio:aspect_ratio,'file_change_event':e};
                    this.dialogRefImgCrop = this.dialog.open(ImageCropDirective,{data: data});
                    this.dialogRefImgCrop.afterClosed().subscribe(result => {
                      if(result){
                        this._cookieService.put('temp_dir',result.dir_name);
                        this.widget.insertables[block_index].properties[temp_index].value=GlobalVariable.S3_URL+result.media_dir;
                        this.widget.insertables[block_index].properties[temp_index].type=temp_arr['type'];
                        this.widget.insertables[block_index].properties[temp_index].url=GlobalVariable.S3_URL+result.media_dir;

                        // this.widget.insertables[block_index].properties.forEach(item=>{
                        //   if(item.selector==imgFor){ 
                        //     item.value = GlobalVariable.S3_URL+result.media_dir;
                        //     item.type = temp_arr['type'];
                        //     item.url = GlobalVariable.S3_URL+result.media_dir;
                        //   }
                        // });
                        this.modelChange();
                      }
                    });  

                };  

                img.src = srcElm['result'];

            }
        }  
      }
    }

   

    insertUrl(imgFor: string, block_index:number){

      this.widget.insertables[block_index].properties.forEach(item=>{
        if(item.selector==imgFor && item.url!=null && item.url.trim()!=''){
          item.value = item.url;
          item.type = 1; // image upload type - 1 i.e insert link
          item._file = {};
          this.modelChange();
        }
      });
      
    } 


    onDropboxLoad(imgFor:string, block_index:number){

      let that = this;
      
      // dropbox options
      var options = {

          // Required. Called when a user selects an item in the Chooser.
          success: function(files) {
              that.onDropboxSucc(files, imgFor, block_index);
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

    onDropboxSucc(files:any, imgFor:string, block_index:number){
        
       
      if(!this._globalService.check_file_size(files[0].bytes)){
          this._globalService.showToast('Maximum 2MB of file size is allowed');
      }else{
          var url = '';
          url = files[0].link;

          this.widget.insertables[block_index].properties.forEach(item=>{
            if(item.selector==imgFor){

              item.value = url;
              item.type = 1; // image upload type - 1 i.e dropbox upload
              item._file = {};

            }
          });
          this.modelChange();
      }
        
    }

}



@Component({
  templateUrl: './add_form_field.html',
  providers: [],
})
export class FormAddEditFieldComponent implements OnInit { 
  public response: any;
  public errorMsg: string;
  public successMsg: string;
  public formModel: any = {};
  private sub: any;
  public show_desc:boolean=false;
  public add_edit:string;


  constructor(
    public _globalService:GlobalService,
    private _cookieService:CookieService,
    private dialogRef: MatDialogRef<FormAddEditFieldComponent>,
    public dialog: MatDialog,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {

    dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
               containerElem.classList.remove('pop-box-up');
      });
  }
  
  ngOnInit(){
      
    this.add_edit = this.data.type;
    this.formModel = Object.assign({},this.data.field_data);
    if(this.data.field_data.input_type=='Checkbox' || this.data.field_data.input_type=='Radio' || this.data.field_data.input_type=='Dropdown'){
      this.formModel.custom_values = this.data.field_data.custom_values.join(',')  
    }
    
    this.formModel.is_optional = (this.data.field_data.value_required=='y')?1:0;
    this.OnchangeField(this.formModel.input_type);
    
  }

  OnchangeField(fieldVal){
    if((fieldVal=='Checkbox')||(fieldVal=='Radio')||(fieldVal=='Dropdown')){this.show_desc=true;}
    else{this.show_desc=false;}
  }  
  addEditField(form: any){
      
    let data:any = {};

    data.field_label = this.formModel.field_label;
    data.input_type = this.formModel.input_type;
    if(this.formModel.default_values){
      data.default_values = this.formModel.default_values;
    }else{
      data.default_values = '';
    }

    if(this.formModel.custom_values){
      data.custom_values = this.formModel.custom_values.split(',');
    }else{
      data.custom_values = '';
    }

    if(this.formModel.is_optional){
      data.value_required = 'y';
    }else{
      data.value_required = 'n';
    }

    this.dialogRef.close(data);

  }

  closeDialog(){
    this.dialogRef.close();
  }

}

