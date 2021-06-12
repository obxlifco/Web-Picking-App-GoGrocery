import { Component,OnInit,Input,Optional} from '@angular/core';
import { GlobalService } from '../global/service/app.global.service';
import { Router,ActivatedRoute } from '@angular/router';
import { PageService } from './manage.store.service';
import { GlobalVariable } from '../global/service/global';
import { DialogsService} from '../global/dialog/confirm-dialog.service';


@Component({
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class ManageStoreComponent { 
  public tabIndex: number;
  public parentId: number = 0;
  childData = {};
  /**
  * Inject Dependencies
  *  
  */
  constructor(public _globalService:GlobalService){
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      // pass data to global grid component
      this.childData = {
        table : 'EngageboostPages',
        heading : 'Ecommerce Pages',
        ispopup:'N',
        tablink:'manage_store',
        is_import: 'N',
        is_export: 'Y',
        tabparrentid:this.parentId,
        screen:'list'
      }
    }
}
  
@Component({
  templateUrl: 'templates/add-manage-store.html',
  providers: [PageService]
})
export class ManageStoreAddEditComponent implements OnInit { 
  public errorMsg: string;
  public successMsg: string;
  public formModel: any = {};
  public tabIndex: number;
  public parentId: number = 0;
  public ipaddress: any;
  /**
  * Inject Dependencies
  *  
  */  
  constructor(
    private _pageService:PageService,
    public _globalService:GlobalService,
    private _router: Router,
    private _route: ActivatedRoute,
    private _dialogsService:DialogsService
  ) {
    this.ipaddress = _globalService.getCookie('ipaddress');
  }

  /**
  * Initialization
  *  
  */  
  ngOnInit(){

    this.tabIndex = +this._globalService.getCookie('active_tabs');
    this.parentId = this._globalService.getParentTab(this.tabIndex);
    this._route.params.subscribe(params => { // pick id from the route url
        this.formModel.id = +params['id']; // (+) converts string 'id' to a number
        if(this.formModel.id){
          this._router.navigate(['/manage_store']);
          
            this._pageService.pageLoad(this.formModel.id).subscribe(
            data => {
                if(data.status){
                  let parser = document.createElement('a');
                  parser.href = GlobalVariable.BASE_Frontend_URL;
                  let editor_url: string = '';
                  if(this._globalService.getWebsiteId()==1){
                    editor_url = GlobalVariable.BASE_Frontend_URL+'editor/page/'+data.api_status.url;
                  } else {
                    let host_name = parser.hostname;
                    if(host_name.indexOf('www')>-1){
                      host_name = host_name.split('www.')[1];
                    }
                    editor_url = parser.protocol +'//'+ this._globalService.getWebsiteName().toLowerCase() +'.'+host_name+'/editor/page/'+data.api_status.url;
                  }
                  // let editor_url: string = GlobalVariable.BASE_Frontend_URL+(this._globalService.getWebsiteName()).toLowerCase()+'/editor/page/'+data.api_status.url;
                  let external = window.open(editor_url, "_blank");
                  if(external==null){
                    this._dialogsService.alert('Warning', 'Please allow popup for the website from browser.').subscribe(res => {});
                  }
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

  /**
  * create slug of the page
  * @param val - string
  *  
  */  
  createUrl(val:string){

    var slug = '';
    slug = val.toLowerCase().replace(/[^\w ]+/g,'-').replace(/ +/g,'-');

    this.formModel.url = slug;
  }

  /**
  * submit form to add new page
  * @param form - any
  *  
  */
  addPage(form:any){

    this.errorMsg = '';
    var data: any = {};
    data = Object.assign({},this.formModel);
    data.ip_address=this.ipaddress;
    data.createdby_id = this._globalService.getUserId();
    data.modifiedby_id = this._globalService.getUserId();

    data.company_website_id = this._globalService.getWebsiteId();
    data.layout = 1;
    data.device = 'web';
    console.log(data);
    
    this._pageService.pageAdd(data).subscribe(
        data => {
            if(data.status==1){
              this._globalService.deleteTab(this.tabIndex,this.parentId);
              this._router.navigate(['/manage_store']);

              let parser = document.createElement('a');
              parser.href = GlobalVariable.BASE_Frontend_URL;
              
              let editor_url: string = '';
              if(this._globalService.getWebsiteId()==1){
                editor_url = GlobalVariable.BASE_Frontend_URL+'editor/page/'+this.formModel.url;
              }else{
                
                let host_name = parser.hostname;
                if(host_name.indexOf('www')>-1){
                  host_name = host_name.split('www.')[1];
                }

                editor_url = parser.protocol +'//'+ this._globalService.getWebsiteName().toLowerCase() +'.'+host_name+'/editor/page/'+this.formModel.url;
              }

              // let editor_url: string = GlobalVariable.BASE_Frontend_URL+(this._globalService.getWebsiteName()).toLowerCase()+'/editor/page/'+this.formModel.url;
              let external = window.open(editor_url, "_blank");
              if(external==null){
                this._dialogsService.alert('Warning', 'Please allow popup for the website from browser.').subscribe(res => {});
              }
            }else{
              this.errorMsg = data.message;
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

}




