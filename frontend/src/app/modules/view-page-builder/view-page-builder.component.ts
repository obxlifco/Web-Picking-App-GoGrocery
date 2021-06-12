import { Component, OnInit, ViewChild,ElementRef,ComponentFactoryResolver,ViewContainerRef,ViewChildren,QueryList, Inject, PLATFORM_ID } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { EditWidgetComponent } from './edit-widget/edit-widget.component';
import { Widget } from '../../global/widget/widget';
import { WidgetsService } from '../../global/widget/widgets.service';
import { GlobalService } from '../../global/service/app.global.service';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import {CategoryService} from '../../global/service/category.service';
import { CookieService } from 'ngx-cookie';
import { Router,ActivatedRoute } from '@angular/router';
import {AddEditPageComponent, ManagePageComponent, ManageNavigationComponent} from './page-setup/page.setup.component';
import { WidgetComponent } from '../../global/widget/widget.interface';
import { PageSetupService } from './page-setup/page.setup.service';
import {DOCUMENT} from '@angular/platform-browser';
import  html2canvas from "html2canvas";
import { WINDOW } from '@ng-toolkit/universal';
import {CdkDragDrop, moveItemInArray, transferArrayItem, copyArrayItem} from '@angular/cdk/drag-drop';
import { isPlatformBrowser } from '@angular/common';

declare var CKEDITOR: any;
@Component({
  selector: 'app-view-page-builder',
  templateUrl: './view-page-builder.component.html',
  styleUrls: ['./view-page-builder.component.css'],
  providers: [PageSetupService]
})
export class ViewPageBuilderComponent implements OnInit {
  public widgets: any;
  public receivedData: Array<any> = [];
  public showWidgetPanel: Boolean = false;
  public editData: any = {};
  public ipaddress:string;
  public page_slug: string;
  public pageId:number;
  public templateId:number;  
  public widget_category:any;
  public editor_config:any = {};
  public editorType:number;
  public rootURI:string;
  public cdnRootUrl:string = 'https://d2vltvjwlghbux.cloudfront.net/frontend/';
  public frontend_url:string;
  public selectedIndex:number;
  public selected_lang:string = 'en';
  public company_name:string = '';
  public is_dist:boolean = false;
  public website_id:number;
  public hostUrl:any;
  public currentYear=(new Date()).getFullYear();
  // Selector for dynamic widget data fetch during edit time
  public dynamicWidgetSelector = {
    '20' : ['category_id'],
    '19' : ['category_id_1','category_id_2','category_id_3','category_id_4','category_id_5','category_id_6','category_id_7','category_id_8'],
    '18' : ['brand_id_1','brand_id_2','brand_id_3','brand_id_4','brand_id_5']

  };
  @ViewChild("emailTemp", {read: ElementRef}) emailTemp: ElementRef;
  @ViewChild("pageTemp", {read: ElementRef}) pageTemp: ElementRef;
  @ViewChild(EditWidgetComponent) child: EditWidgetComponent;
  @ViewChildren('dynamic', {read: ViewContainerRef}) public widgetTargets: QueryList<ViewContainerRef>;  
  constructor(@Inject(WINDOW) private window: Window,
      @Inject(DOCUMENT) private document: Document,
      public dialog: MatDialog, 
      private widgetsService: WidgetsService,
      public elementRef: ElementRef, 
      public domSanitizer:DomSanitizer,
      public _globalService:GlobalService, 
      public _cookieService:CookieService,
      private _router: Router,
      private _route: ActivatedRoute,
      private dialogsService: DialogsService,
      private componentFactoryResolver: ComponentFactoryResolver,
      public _pageSetupService:PageSetupService,
      public _categoryService :CategoryService,
      @Inject(PLATFORM_ID) private platformId: Object
 
    ) { 
        this.frontend_url =  this.window.location.origin+'/'+this.window.location.pathname.split('/')[1];
        this.hostUrl = this.document.location.protocol+'//'+this.document.location.hostname+'/';
        this.rootURI      = this.window.location.origin+'/';
        this.company_name = _globalService.getFrontedCompanyName();
        this.ipaddress = _globalService.getCookie('ipaddress');
        this.editor_config = {uiColor: '#ffffff',
                        toolbar: [
                                { name: 'document', items: [ 'Source', 'Templates' ] },
                                { name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript' ] },
                                { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] },
                                { name: 'links', items: [ 'Link', 'Unlink', 'Anchor' ] },
                                { name: 'insert', items: [ 'Image', 'Table', 'HorizontalRule', 'SpecialChar' ] },
                                { name: 'styles', items: [ 'FontSize' ] },
                                { name: 'colors', items: [ 'TextColor', 'BGColor' ] },
                                { name: 'tools', items: [ 'Maximize', 'ShowBlocks' ] },
                              ]         
                };
        _route.url.subscribe(() => {
            this.editorType = _route.snapshot.data.editorType;
        });
        this._globalService.globalDataChange$.subscribe(value => {
            let globalData = this._cookieService.getObject('globalData');
            //console.log('Global Data service');
            //console.log(globalData);
            //console.log(globalData['website_id']);
            if(globalData['website_id'] > 1) {
              this.is_dist = true;
              this.website_id = globalData['website_id'];
            } else {
              this.is_dist = false;
              this.website_id = 1;
            }
        },
        err => {
            console.log(err);
        });      
  }

  setActive(index:number) {
    this.widget_category.forEach(item=>{
      if(item.id==index){
        item.active = true;
        item.hover = false;
        this.widgets = this.widgetsService.getWidgets(item.id,this.editorType, this.website_id);
      }else{
        item.active = false;
        item.hover = true;
      }
    });
  }

  closeWidgetCat(event:any){ 
    event.stopPropagation();
    this.widget_category.forEach((item)=>{
      item['active'] = false;
      item['hover'] = false;
    });
  }

  ngOnInit() {
   
    this._cookieService.remove('temp_dir');
    if (isPlatformBrowser(this.platformId)) {
      this.widget_category = this.widgetsService.getWidgetCategories();
      this.child = new EditWidgetComponent(this.domSanitizer,this.dialog,this._globalService,this.widgetsService,this._cookieService,this._pageSetupService);
      this._route.params.subscribe(params => {
          this.reset();  
          if(this.editorType==1){
            this.page_slug = params['slug']; 
            let data:any = {url: this.page_slug,template_id:1,company_website_id:1, lang: this.selected_lang}
           
            this.widgetsService.pageLoad(data).subscribe(
              data => { 
                if(data.status){ 
                  this.pageId = data.page_id;
                  data.cms_widgets.forEach((item,index)=>{
                    let data:any = JSON.parse(item.property_value);
                    let widget = new Widget(data.id,data.is_distributor,data.widget_category,data.label,data.type,data.favicon,data.component,this.widgetsService.getWidgetTemplate(data.id,this.editorType),data.insertables);
                    //Don't want by reference
                    //this was a HUGE pain in my arse. Some reason when getting insertables it'd copy object by reference, not making a new obj
                    widget = new Widget(widget.getID(), widget.getIsDistributor(),widget.getWidgetCategory(),widget.getLabel(), widget.getType(), widget.getFavicon(), widget.getComponent(),widget.getHtmlTemplate(), JSON.parse(JSON.stringify(widget.getInsertables())));
                    widget['widget_id'] = data.widget_id;
                    this.receivedData.push({dragData: widget});
                    setTimeout(() => {
                      if(widget.getType()==2){ 
                          var hElement: HTMLElement = this.elementRef.nativeElement;
                          setTimeout(()=>{
                            let inserted_editor = hElement.getElementsByClassName('inserted');
                            let editorID="editor"+data['widget_id'];
                            let config = this.editor_config;
                            for(let i=0; i<inserted_editor.length; i++){
                              let classList: any = inserted_editor[0].classList;
                              editorID = editorID+'_'+classList[0];
                              let dynamic_indexes = classList[0].split('-');
                              inserted_editor[i].innerHTML = '<div id="'+editorID+'"  contenteditable="true" >'+widget.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value+'</div>';  
                              CKEDITOR.disableAutoInline = true;
                              CKEDITOR.inline( editorID, config );             
                            
                              CKEDITOR.instances[ editorID ].on('blur', (evt) => { 
                                let editor_content = CKEDITOR.instances[editorID].getData();
                                this.receivedData.forEach(item=>{
                                  if(item.dragData.widget_id==data['widget_id']){
  
                                    item.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value = editor_content;
                                    this.assignEditor(editorID,dynamic_indexes,data['widget_id']);
                                  }
                                });
                              });
                              inserted_editor[i].classList.remove('inserted');
                            }
                          },200);                        
                      }else{
                        let target = this.widgetTargets.toArray()[index];
                        let widgetComponent = this.componentFactoryResolver.resolveComponentFactory(this.widgetsService.components[this.receivedData[index].dragData.component]);                      
                        target.clear();
                        let cmpRef: any = target.createComponent(widgetComponent);
                        (<WidgetComponent>cmpRef.instance).data = this.receivedData[index].dragData.insertables;
                        (<WidgetComponent>cmpRef.instance).isCMS = true;
                      }
                    });
                  });
                }
              },
              err => {
                this._globalService.showToast('Something went wrong. Please try again.');
              },
              function(){
                //completed callback
              }
            );
          }else if(this.editorType==2){
            this.templateId = params['slug'];
            let data:any = {template_id: this.templateId,company_website_id:this._globalService.getWebsiteId()}
            this.widgetsService.emailTemplateLoad(data).subscribe(
              data => {
                if(data.status){
                  
                  data.cms_widgets.forEach((item,index)=>{
  
                    let widget = new Widget(item.id,item.is_distributor,item.widget_category,item.label,item.type,item.favicon,item.component,this.widgetsService.getWidgetTemplate(item.id,this.editorType),item.insertables);
                   
                    //Don't want by reference
                    //this was a HUGE pain in my arse. Some reason when getting insertables it'd copy object by reference, not making a new obj
                    widget = new Widget(widget.getID(), widget.getIsDistributor(),widget.getWidgetCategory(),widget.getLabel(), widget.getType(), widget.getFavicon(), widget.getComponent(),widget.getHtmlTemplate(), JSON.parse(JSON.stringify(widget.getInsertables())));
                    widget['widget_id'] = data.widget_id;
                    this.receivedData.push({dragData: widget});
  
                    setTimeout(() => {
                      if(widget.getType()==2){ 
                      
                          var hElement: HTMLElement = this.elementRef.nativeElement;
  
                          setTimeout(()=>{
                            let inserted_editor = hElement.getElementsByClassName('inserted');
                            let editorID="editor"+data['widget_id'];
                            let config = this.editor_config;
  
                            for(let i=0; i<inserted_editor.length; i++){
                              
                              let classList: any = inserted_editor[0].classList;
                              editorID = editorID+'_'+classList[0];
                              let dynamic_indexes = classList[0].split('-');
                              inserted_editor[i].innerHTML = '<div id="'+editorID+'" contenteditable="true">'+widget.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value+'</div>';  
                              CKEDITOR.disableAutoInline = true;
                              CKEDITOR.inline( editorID, config );             
                            
                              CKEDITOR.instances[ editorID ].on('blur', (evt) => { 
                                let editor_content = CKEDITOR.instances[editorID].getData();
                                this.receivedData.forEach(item=>{
                                  if(item.dragData.widget_id==data['widget_id']){
  
                                    item.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value = editor_content;
                                    this.assignEditor(editorID,dynamic_indexes,data['widget_id']);
                                  }
                                });
                              });
  
                              inserted_editor[i].classList.remove('inserted');
  
                            }
  
                          },200);
                          
                      }else{
                        let target = this.widgetTargets.toArray()[index];
                        let widgetComponent = this.componentFactoryResolver.resolveComponentFactory(this.widgetsService.components[this.receivedData[index].dragData.component]);  
                        
                        target.clear();
                        let cmpRef: any = target.createComponent(widgetComponent);
                        (<WidgetComponent>cmpRef.instance).data = this.receivedData[index].dragData.insertables;
                        (<WidgetComponent>cmpRef.instance).isCMS = true;
                      }
                    });  
                    
                    
  
                  });
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
      });
    }

    
  }

  reset() {
    this.receivedData = [];
  }

  setSection(index){
    this.selectedIndex = index;
  }

  editItem(index) {

    var thisWidget: Widget = this.receivedData[index].dragData;
    thisWidget = this.reflectLiveDataInWidgetEdit(thisWidget);


    /*console.log("**************** Widget data *******************");
    console.log(thisWidget);*/
    /*console.log(this)*/
    // var thisWidget: Widget = this.receivedData[index];

    if(this.receivedData[index].dragData.type!=2){

      this.editData = { widget: thisWidget, widgetIndex: index };
      this.showWidgetPanel = true;
    }else{
      this.showWidgetPanel = false;
    }
    
    if(this.child){
      this.child.changeEvnt(this.editData);  
    }
  }
  /**
   * Method for reflecting current data
   * This method is for those widget where live chnages need to be reflected
   * This is somehow static,and different for different widget id
   * The selector is very inportant
   * @access public
  */
  reflectLiveDataInWidgetEdit(widgetObject) {
    this.getWidgetDataOnRuntime(widgetObject);
    return widgetObject;


  }
  async getWidgetDataOnRuntime(widgetObject) {
    let promiseData:Promise<any>;
    let formattedWidgetData = widgetObject;
    let widgetId = widgetObject['id'];
    let type = widgetObject['type'];
    if(widgetObject['type'] == 1) {
      if(widgetId == 20 && this.dynamicWidgetSelector[widgetId] && this.dynamicWidgetSelector[widgetId].length > 0) {
        if(this.dynamicWidgetSelector[widgetId].includes('category_id')) {
          promiseData =  await this._categoryService.getParentCategoryList().toPromise();
          formattedWidgetData = this.formatWidgetObjectWithPromiseData(widgetObject,promiseData,'category_id');
        }
      }
      if(widgetId == 19 && this.dynamicWidgetSelector[widgetId] && this.dynamicWidgetSelector[widgetId].length > 0) {
        if(
             this.dynamicWidgetSelector[widgetId].includes('category_id_1') || 
             this.dynamicWidgetSelector[widgetId].includes('category_id_2') ||
             this.dynamicWidgetSelector[widgetId].includes('category_id_3') ||
             this.dynamicWidgetSelector[widgetId].includes('category_id_4') || 
             this.dynamicWidgetSelector[widgetId].includes('category_id_5') ||
             this.dynamicWidgetSelector[widgetId].includes('category_id_6') ||
             this.dynamicWidgetSelector[widgetId].includes('category_id_7')

          ) {
          promiseData =  await this._categoryService.getShopByCategoryData().toPromise();

          formattedWidgetData = this.formatWidgetObjectWithPromiseData(widgetObject,promiseData,this.dynamicWidgetSelector[widgetId]);
        }
      }
      // For dynamic brands
      if(widgetId == 18 && this.dynamicWidgetSelector[widgetId] && this.dynamicWidgetSelector[widgetId].length > 0) {
        if(
             this.dynamicWidgetSelector[widgetId].includes('brand_id_1') || 
             this.dynamicWidgetSelector[widgetId].includes('brand_id_2') ||
             this.dynamicWidgetSelector[widgetId].includes('brand_id_3') ||
             this.dynamicWidgetSelector[widgetId].includes('brand_id_4') || 
             this.dynamicWidgetSelector[widgetId].includes('brand_id_5') 
          ) {
          promiseData =  await this._categoryService.getBrands().toPromise();

          formattedWidgetData = this.formatWidgetObjectWithPromiseData(widgetObject,promiseData,this.dynamicWidgetSelector[widgetId]);
        }
      }



    }
    return formattedWidgetData;
  }
  formatWidgetObjectWithPromiseData(widgetObject,promiseData,requestType:any) {
      if(promiseData['status'] == 1 && promiseData['data']) {
        widgetObject['insertables'].forEach(insertableData => {
          insertableData['properties'].forEach(propertiesData => {
            if(Array.isArray(requestType)) {
              if(requestType.includes(propertiesData['selector'])) {
                propertiesData['options'] = promiseData['data'];

              }

            } else {
              if(propertiesData['selector'] == requestType) {
                propertiesData['options'] = promiseData['data'];
              }

            }
            
          })
        })
      } 
     return widgetObject;
  }


  deleteWidget($event){
    this.receivedData.splice($event, 1);
    this.showWidgetPanel = false;
  }

  closeWidget(){
    this.showWidgetPanel = false;
  }

  updateWidget($event){

    this.loadComponents();
  }

  loadComponents(index?:any){
    if(index != undefined){
      if(this.receivedData[index].dragData.type!=2){
        let target = this.widgetTargets.toArray()[index];
        let widgetComponent = this.componentFactoryResolver.resolveComponentFactory(this.widgetsService.components[this.receivedData[index].dragData.component]);  
        target.clear();
        let cmpRef: any = target.createComponent(widgetComponent);
        (<WidgetComponent>cmpRef.instance).data = this.receivedData[index].dragData.insertables;
        (<WidgetComponent>cmpRef.instance).isCMS = true;
      }
    }else{
      this.receivedData.forEach((item,index)=>{
        if(this.receivedData[index].dragData.type!=2){
          let target = this.widgetTargets.toArray()[index];
          let widgetComponent = this.componentFactoryResolver.resolveComponentFactory(this.widgetsService.components[this.receivedData[index].dragData.component]);  
          target.clear();
          let cmpRef: any = target.createComponent(widgetComponent);
          (<WidgetComponent>cmpRef.instance).data = this.receivedData[index].dragData.insertables;
          (<WidgetComponent>cmpRef.instance).isCMS = true;
        }
      });
    }
    
  }
  drop(event: CdkDragDrop<string[]>){ 
		if (event.previousContainer === event.container) {
			 moveItemInArray(event.container.data, event.previousIndex, event.currentIndex); 
		} 
		else { 
			let dragData={ 
				dragData:event.previousContainer.data[event.previousIndex]
			}; 
			this.transferDataSuccess(dragData,event);
		 } 
    }
    
  transferDataSuccess($event: any,event: CdkDragDrop<string[]>) {
    var widget: Widget = $event.dragData;
    //Don't want by reference
    //this was a HUGE pain in my arse. Some reason when getting insertables it'd copy object by reference, not making a new obj
    $event.dragData = new Widget(widget.getID(), widget.getIsDistributor(),widget.getWidgetCategory(),widget.getLabel(), widget.getType(), widget.getFavicon(), widget.getComponent(),widget.getHtmlTemplate(), JSON.parse(JSON.stringify(widget.getInsertables())));
    
    $event.dragData['widget_id'] = Math.floor((Math.random() * 100000) + 1);
    // this.receivedData.push($event);
    // const index=this.receivedData.length -1;

    const index = event.currentIndex;
    this.receivedData.splice(index,0,$event)
    
      setTimeout(() => {
        if(widget.getType()!=2){
          this.loadComponents(index);
        }
      });  
      
    if(widget.getType()==2){ 
      var hElement: HTMLElement = this.elementRef.nativeElement;
      setTimeout(()=>{
        let inserted_editor = hElement.getElementsByClassName('inserted');
        let inserted_editor_len = inserted_editor.length;
        let editorID="editor"+$event.dragData.widget_id;
        let config = this.editor_config;

        for(let i=0; i<inserted_editor_len; i++){
          
          let classList: any = inserted_editor[0].classList;
          let _editorID = editorID+'_'+classList[0];
          let dynamic_indexes = classList[0].split('-');
          inserted_editor[0].innerHTML = '<div id="'+_editorID+'" contenteditable="true">'+$event.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value+'</div>';  
          CKEDITOR.disableAutoInline = true;
          CKEDITOR.inline( _editorID, config );             
        
          CKEDITOR.instances[ _editorID ].on('blur', (evt) => { 
            let editor_content = CKEDITOR.instances[_editorID].getData();
            this.receivedData.forEach(item=>{
              if(item.dragData.widget_id==$event.dragData.widget_id){
                item.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value = editor_content;
                this.assignEditor(_editorID,dynamic_indexes,$event.dragData.widget_id);
              }
            });
          });

          inserted_editor[0].classList.remove('inserted');

        }

      },200);
      
    }

  }  

  assignEditor(editorID:string,dynamic_indexes:any,widget_id:string){

    var hElement: HTMLElement = this.elementRef.nativeElement;
    setTimeout(()=>{
        let inserted_editor = hElement.getElementsByClassName('inserted');
        let inserted_editor_len = inserted_editor.length;
        let config = this.editor_config;
        if(inserted_editor_len==1){

            this.receivedData.forEach(item=>{
              if(item.dragData.widget_id==widget_id){
                inserted_editor[0].innerHTML = '<div id="'+editorID+'" contenteditable="true">'+item.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value+'</div>';  
                CKEDITOR.disableAutoInline = true;
                CKEDITOR.inline( editorID, config );             
                
                CKEDITOR.instances[ editorID ].on('blur', (evt) => { 
                  let editor_content = CKEDITOR.instances[editorID].getData();
                  
                  item.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value = editor_content;
                  this.assignEditor(editorID,dynamic_indexes,widget_id);
                });

                inserted_editor[0].classList.remove('inserted');
              }
              
            });
          
        }else if(inserted_editor_len>1){
          editorID="editor"+widget_id;
          for(let i=0; i<inserted_editor_len; i++){
            
            this.receivedData.forEach(item=>{
              if(item.dragData.widget_id==widget_id){

                let classList: any = inserted_editor[0].classList;
                let _editorID = editorID+'_'+classList[0];
                let dynamic_indexes = classList[0].split('-');
                inserted_editor[0].innerHTML = '<div >'+item.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value+'</div>';  
                CKEDITOR.disableAutoInline = true;
                CKEDITOR.inline( _editorID, config );             
              
                CKEDITOR.instances[ _editorID ].on('blur', (evt) => { 
                  let editor_content = CKEDITOR.instances[_editorID].getData();
                  
                  item.dragData.insertables[dynamic_indexes[0]].properties[dynamic_indexes[1]].value = editor_content;
                  this.assignEditor(_editorID,dynamic_indexes,widget_id);
                });

                inserted_editor[0].classList.remove('inserted');
              }
            });    

          }
        }
      },200);
  }

  dialogRefAddPage: MatDialogRef<AddEditPageComponent> | null;
  openAddPageDialog(page_id:number=0){

    let data:any = { page_id: page_id};
    this.dialogRefAddPage = this.dialog.open(AddEditPageComponent,{data: data,maxHeight:500,maxWidth:500});
    this.dialogRefAddPage.afterClosed().subscribe(result => {

    });
      
  }

  dialogRefManagePage: MatDialogRef<ManagePageComponent> | null;
  openManagePageDialog(){

    let data:any = { };
    this.dialogRefManagePage = this.dialog.open(ManagePageComponent,{data: data,maxHeight:500,maxWidth:500});
    this.dialogRefManagePage.afterClosed().subscribe(result => {
      
    });
      
  }  

  dialogRefManageNavigation: MatDialogRef<ManageNavigationComponent> | null;
  openNavigationDialog(flag:number = 0){
    
    let data:any = { header_footer: flag };
    this.dialogRefManageNavigation = this.dialog.open(ManageNavigationComponent,{data: data,maxHeight:500,maxWidth:500});
    this.dialogRefManageNavigation.afterClosed().subscribe(result => {
      
    });
  }

  AddEditCMS(){ 
    this.selectedIndex = null;
    
    if(this.editorType==1) {
        let data:any = {};
        data.lang = this.selected_lang;
        data.company_website_id = 1;
        data.template_id = 1;
        data.page_id = this.pageId;
        data.ip_address = this.ipaddress;
        data.createdby = this._globalService.getUserId();
        data.updatedby = this._globalService.getUserId();
        data.widgets = [];

        let widgets: any = JSON.parse(JSON.stringify(this.receivedData));

        widgets.forEach(item=>{
            delete item.dragData['htmlTemplate'];
            if(item.dragData.type==3){
                  item.dragData.insertables[0].fields.forEach(field=>{
                    if(field.input_type=='Dropdown' || field.input_type=='Radio' || field.input_type=='Checkbox'){
                      if(field.custom_values.length>0){
                        field.custom_values = field.custom_values.join(',');
                      }
                    }
                  });
            }
            data.widgets.push(item.dragData);
        });
        /*console.log("************* Receive data **************");
        console.log(data);*/
        html2canvas( this.pageTemp.nativeElement )
            .then((canvas) => {
              var img = canvas.toDataURL();          
              let blobObject = this.dataURItoBlob(img);          
              let formData = new FormData();
              formData.append('file', blobObject);
              formData.append('data',JSON.stringify(data));
              console.log(formData);
              this.dialogsService.confirm('Warning', 'Do you really want to save this page content ?').subscribe(res => {
                  if(res){
                    this._globalService.showLoaderSpinner(true);
                    this.widgetsService.cmsAddEdit(formData).subscribe(
                        data => {
                         if(data.status){
                           this._globalService.showToast('Page content successfully changed');
                         }
                        },
                        err => {
                          this._globalService.showLoaderSpinner(false);  
                          this._globalService.showToast('Something went wrong. Please try again.');
                        },
                        ()=>{
                            //completed callback
                            this._globalService.showLoaderSpinner(false);
                        }
                    );
                  }
              });         
            })
            .catch(err => {
              console.log("error canvas", err);
            });
    } else if(this.editorType==2) {      
          let data:any = {};
          data.company_website_id = this._globalService.getWebsiteId();
          data.template_id = this.templateId;
          data.ip_address = this.ipaddress;
          data.createdby = this._globalService.getUserId();
          data.updatedby = this._globalService.getUserId();
          data.widgets = [];
          let widgets: any = JSON.parse(JSON.stringify(this.receivedData));
          widgets.forEach(item=>{
            delete item.dragData['htmlTemplate'];
            data.widgets.push(item.dragData);
          });
          data.template_data = this.emailTemp.nativeElement.innerHTML;         
          var sheet = document.createElement('style')
          sheet.innerHTML = "div {color:red;overflow:hidden;}";
          document.body.appendChild(sheet);          
          html2canvas( this.emailTemp.nativeElement )
            .then((canvas) => {
              var img = canvas.toDataURL();              
              let blobObject = this.dataURItoBlob(img);              
              let formData = new FormData();
              formData.append('file', blobObject);
              formData.append('data', JSON.stringify(data));
              this.dialogsService.confirm('Warning', 'Do you really want to save this email content ?').subscribe(res => {
                if(res){
                  this._globalService.showLoaderSpinner(true);
                  this.widgetsService.emailTemplateAddEdit(formData).subscribe(
                      data => {
                       if(data.status){
                         this._globalService.showToast('Email content successfully changed');
                       }
                      },
                      err => {
                        this._globalService.showLoaderSpinner(false);
                        this._globalService.showToast('Something went wrong. Please try again.');
                      },
                      ()=>{
                          //completed callback
                          this._globalService.showLoaderSpinner(false);
                      }
                  );
                }
              });          
            })
            .catch(err => {
              console.log("error canvas", err);
            });
    }
    
  }
  setLang(lang:string){
    this.selected_lang = lang;
    this.ngOnInit();
  }
  // convert base64 image url to blob image 
  dataURItoBlob(dataURI: string) {
    let byteString: any;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
      byteString = atob(dataURI.split(',')[1]);
    else
      byteString = decodeURI(dataURI.split(',')[1]);
    // separate out the mime component
    let mimeString: any = dataURI.split(',')[0].split(':')[1].split(';')[0];
    // write the bytes of the string to a typed array
    let blob: any = new Uint8Array(byteString.length);
    for (let i = 0; i < byteString.length; i++) {
      blob[i] = byteString.charCodeAt(i);
    }
    return new Blob([blob], {
      type: mimeString
    });
  }
  /**
   * Method for handaling scroll
   * @access public
  */
  handleDrag(event) {
    /*console.log("********************* Event *****************");
    console.log(event);*/
    
    var offset = 400;
    var scrollValueDown = 10;
    var scrollValueUp = -1*scrollValueDown;
    if(event.screenY > 0 && event.screenY < offset){
      window.scrollBy(0, scrollValueUp) // up
    }

    if(event.screenY > (window.outerHeight - offset) && event.screenY < window.outerHeight){
      window.scrollBy(0, scrollValueDown) // down
    }
    let currentElement = document.elementFromPoint(event.screenX,event.screenY);
    console.log(currentElement);
    

  }
  handleDrop(event) {
    console.log(event)

  }


}