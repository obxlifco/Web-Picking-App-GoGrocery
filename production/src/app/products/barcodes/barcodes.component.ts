import { GlobalService } from '../../global/service/app.global.service';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Component, OnInit, OnDestroy, Optional, Inject,ElementRef} from '@angular/core';
import { BarcodeService } from './barcode.service';
import {Global} from '../../global/service/global';
import {DOCUMENT} from '@angular/platform-browser';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class BarcodesComponent {

  public tabIndex: number;
  public parentId: number = 0;
  
	childData = {};
	constructor(
    private _globalService:GlobalService,
    public dialog: MatDialog,
    private dialogsService: DialogsService,
    ){
    this.tabIndex = +_globalService.getCookie('active_tabs');
    this.parentId = _globalService.getParentId(this.tabIndex);
    console.log('Bar code working')
    this.childData = {
      table : 'EngageboostMultipleBarcodes',
      heading : 'Barcodes',
      ispopup:'N',
      is_import:'Y',
      is_export: 'Y',
      tablink:'barcodes',
      tabparrentid:this.parentId,
      screen:'list'
    }
    console.log(this.childData)
  }
  
	dialogRefPromotionImport: MatDialogRef<BarcodeImportFileComponent> | null;
  openImportBox(id: any) {
    
		this.dialogRefPromotionImport = this.dialog.open(BarcodeImportFileComponent, { data: 'import_file' });
    this.dialogRefPromotionImport.afterClosed().subscribe(result => {			
    });
  }

}

@Component({
	templateUrl: './templates/import_barcode_file.html',
	providers: [BarcodeService]
})
export class BarcodeImportFileComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public sample_xls: any;
	public sample_csv: any; 
	public xls_file:any;
	public website_id: any;
	public importOpt:any;
  public file_selection_tool: any;
  private userId:number;
	public parentId: number = 0;
	public tabIndex: number;
  public imported_file_name:string;
	
	constructor(
		private _globalService: GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<BarcodeImportFileComponent>,
		public dialog: MatDialog,
		private _cookieService:CookieService,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: any,
    public _barcodeService: BarcodeService,
    
	) { }

	ngOnInit() {
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/MultipleBarcode.xls';
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/MultipleBarcode.csv';
		this.importOpt = 'xls';
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
    this.file_selection_tool = 'No file choosen';
		let userData=this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.website_id=this._globalService.getWebsiteId();
	}

	import_file_barcode(e: Event){
		var files: any = {};
		var target: HTMLInputElement = e.target as HTMLInputElement;
		console.log(target)
		for (var i = 0; i < target.files.length; i++) {
      var file_arr: any = [];

      var reader = new FileReader();
      reader.readAsDataURL(target.files[i]);
      reader.onload = (event) => {
        file_arr['url'] = event.srcElement['result']
      }

      file_arr['_file'] = target.files[i];
      files[this.data] = file_arr;
		}
		var filename = files.import_file._file.name;
    this.file_selection_tool = filename;
    this.xls_file = files.import_file._file;
    var extn = filename.split(".").pop();
    if (extn == 'xls' || extn == 'xlsx') {
    } else {
      this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	send_file_data(form: any) {
    var form_data = new FormData();
    form_data.append("import_file", this.xls_file);
    form_data.append('website_id', this.website_id);
		form_data.append("import_file_type", 'barcode');
    if(this.xls_file != undefined) {
				this._barcodeService.import_barcode_file_data(form_data).subscribe(
					data => {
						console.log('preview barcode')
						console.log(data.file_name)
						this.response = data;
						this.imported_file_name = data.file_name;  
						this._cookieService.putObject('barcode_imported_data','');
						this.load_barcode_preview();
						
					
						this.dialogRef.close();
					},
					err => console.log(err)
				);
    } else {
       this._globalService.showToast('Please choose XLS/XLSX file');
    }
  }
	
	load_barcode_preview(){
	
		var data: any = {};
    var form_data: any = {};
    data.website_id = this._globalService.getWebsiteId();
    data.file_name = this.imported_file_name;
		this._barcodeService.load_barcode_preview(data).subscribe(
		res=>{
      console.log(data)
				this.response = data;    
				let imported_result:any= {};
				this._cookieService.putObject('barcode_imported_data','');
				imported_result.imported_filename = this.imported_file_name;
				imported_result.website_id = this._globalService.getWebsiteId();
				this._cookieService.putObject('barcode_imported_data',imported_result);
				this._globalService.addTab('priviewproducts','barcodes/preview_barcodes','Barcodes Preview',this.parentId)
				this._router.navigate(['/barcodes/preview_barcodes']);
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			}
		)
	}
	
	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
  selector: 'my-app',
  templateUrl: `./templates/barcode_preview.html`,
  providers: [Global,BarcodeService],  
})

export class BarcodePreviewComponent implements OnInit { 
    public response : any;
    public errorMsg: string;
    public successMsg: string;
    public bulk_ids:any = [];
    public columns: any = [];
    public temp_result_list:any=[];
    public result_list:any=[];
    public selectedAll:any=false;
    public tabIndex: number;
    public parentId: number = 0;
    public userId:any;
    public individualRow:any={};

  constructor(  
    public globalService: GlobalService,
    private _globalService: GlobalService,
    private _cookieService:CookieService,
    public dialog: MatDialog,
    private _BarcodeService:BarcodeService,
    private dialogsService: DialogsService,
    @Inject(DOCUMENT) private document: any
  ) { 
  }


 ngOnInit() {
  this.tabIndex = +this.globalService.getCookie('active_tabs');
  this.parentId = this.globalService.getParentTab(this.tabIndex);
  let userData = this._cookieService.getObject('userData');
	let barcode_imported_data = this._cookieService.getObject('barcode_imported_data');   
  this.userId = userData['uid']; 
  let post_data:any = {};
  post_data.file_name = barcode_imported_data['imported_filename'];
  post_data.website_id = this._globalService.getWebsiteId();
	this.columns=[
		{'field_name':'barcode','label':'Product Barcode'},
		{'field_name':'sku','label':'Product SKU'},
	]
  this._BarcodeService.load_barcode_preview(post_data).subscribe(
     data => {
       this.temp_result_list = data.preview_data;
				let that=this;
				this.temp_result_list.forEach(function(item:any){
					if(item.err_flag == 0){
						item.selected = true;
					}
					if(item.selected && item.err_flag == 0){
            that.bulk_ids.push(item.id);
            console.log(that.bulk_ids)
					} 
				});
     },
     err => {
       this.globalService.showToast('Something went wrong. Please try again.');
     },
      function(){
         //completed callback
       }
    );
  }                             

   ////////////////////////////Check/Uncheck//////////////

  toggleCheckAllPreview(event:any) {
		console.log(event)
    //let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
    let that=this;
    that.bulk_ids=[];
    this.selectedAll = event.checked;
    this.temp_result_list.forEach(function(item:any){
      item.selected = event.checked;  
      if(item.selected && item.err_flag == 0){
        that.bulk_ids.push(item.id);
        console.log(that.bulk_ids)
      }
    });
  } 

  toggleCheckPreview(id:any,event:any) {
    console.log(id)
     let that=this;
     this.temp_result_list.forEach(function(item:any) {
       if(item.id==id) {
        item.selected = event.checked;  
        if(item.selected && item.err_flag == 0) {
          that.bulk_ids.push(item.id);
        } else {
          var index = that.bulk_ids.indexOf(item.id);
          that.bulk_ids.splice(index, 1);
          if(that.bulk_ids.length==0){
          } 
        }  
       }
       if(that.bulk_ids.length==1) {
          that.bulk_ids.forEach(function(item_id:any){
          if(item_id==item.id) {
            that.individualRow=item;
          }
          });
        } 
       that.selectedAll=false;     
    });
  }

  BarcodeImportnData (form:any) {
    if(this.bulk_ids.length>0){
      var msg='Are you sure to import selected barcode?'; 
      this.dialogsService.confirm('Warning', msg).subscribe(res => {
        if(res){
          let post_data:any = {};
					let barcode_imported_data = this._cookieService.getObject('barcode_imported_data');
          post_data.file_name = barcode_imported_data['imported_filename'];
          post_data.website_id = this.globalService.getWebsiteId();
					post_data.selected_ids = this.bulk_ids.join(); // convert array to string for selected ids
          this._BarcodeService.show_all_barcode_imported(post_data).subscribe(
           data => {
              this.globalService.deleteTab(this.tabIndex,this.parentId);
              this.globalService.showToast('Barcodes imported successfully');
           },
           err => {
             this.globalService.showToast('Something went wrong. Please try again.');
           },
            function(){
               //completed callback
            }
          );
        }
      });
    } else {
      this.dialogsService.alert('Error', ' Please select atleast one record!').subscribe(res => {});
    } 
  }
}