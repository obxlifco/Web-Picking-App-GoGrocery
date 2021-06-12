import { Component, OnInit, OnDestroy, Optional, Inject,ElementRef} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Global } from '../../global/service/global';
@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class CategoryComponent { 
  public tabIndex: number;
  public parentId: number = 0;
  public add_edit: string;
	childData = {};
	constructor(
      private _globalService:GlobalService,
      private _cookieService: CookieService,
    ){
      _cookieService.remove('cid_add');
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
        table : 'EngageboostCategoryMasters',
        heading : 'Category',
        ispopup:'N',
        is_import: 'N',
        is_export: 'Y',
        tablink:'category',
        tabparrentid:this.parentId,
        screen:'list'
      }
  }
}

@Component({
	templateUrl: 'templates/export-category.html',
	providers: []
})
export class ExportCategoryFile implements OnInit {
	public errorMsg: string = '';
	public formLink: any;
	public download_url: any;
	public sample_csv: any;
	public file_data: any;
	public website_id_new: any;
	public company_id_new: any;
	public importOpt: any;
	constructor(
    private _globalService: GlobalService,
    public dialog: MatDialog,
		private dialogRef: MatDialogRef<ExportCategoryFile>,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formLink =  this.data;
	}
	ngOnInit() {
        this.download_url = window.location.protocol + '//' + window.location.hostname + ':8062/'+this.formLink;
 	}
	closeDialog() {
		  this.dialogRef.close();
	}
}