import { Component, OnInit, Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router } from '@angular/router';
import { PopupImgDirective, ImageUploadUrlDialog } from '../.././global/directive/popup-image.directive';
import { HsncodeService } from './products.hsncode.service';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
	templateUrl: './templates/add_hsncode.html',
  providers: [HsncodeService]
})
export class HsnCodeAddEditComponent implements OnInit { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;


	constructor(
		private _hsnCodeService:HsncodeService,
		private _globalService:GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<HsnCodeAddEditComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        });
        this.ipaddress = _globalService.getCookie('ipaddress'); 
	}
	
	ngOnInit(){
		this.formModel.id = this.data;
		if (this.formModel.id > 0) {
			this._hsnCodeService.loadHscCode(this.formModel.id).subscribe(
				data => {
					this.response = data;
					if (this.formModel.id > 0) {
						this.formModel.id = this.response.api_status.id;
						this.formModel = this.response.api_status;
					} else {
						this.formModel.id = 0;
					}
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		} else {
			this.formModel.id = 0;
		}
	}


	addHsnCode(form: any){ 
		this.errorMsg = '';
		var data: any = {};
		data  =  this.formModel;
		data.website_id = this._globalService.getWebsiteId();
		console.log(data);
		this._hsnCodeService.hsnCodeAddEdit(data, this.formModel.id).subscribe(
			data => {
				this.response = data;
				if (this.response.status == 1) {
					this.closeDialog();
				} else {
					this.errorMsg = this.response.message;
				}
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}
	
    closeDialog(){
		this.dialogRef.close();
	}
}



@Component({
	templateUrl: './templates/hsncode_import.html',
	providers: [HsncodeService]
})
export class HsnCodeImportComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public sample_xls: any;
	public sample_csv: any;
	public xls_file:any;
	public website_id_new: any;
	public importOpt:any;
	
	constructor(
		private _hsnCodeService: HsncodeService,
		private _globalService: GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<HsnCodeImportComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/hsn_master.xls';
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/hsn_master.xls';
		this.importOpt = 'xls';
	}

	importHsnCodeXLS(e: Event) { 
		//console.log(e);
		var files: any = {};
		var target: HTMLInputElement = e.target as HTMLInputElement;
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
		this.xls_file = files.import_file._file;
		var extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
			//this.dialogRef.close(files);
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}	
	
	importHsnCodeCSV(e:Event) {
		this._globalService.showToast('We are working on this.');
	}

	saveHsnCodeImport(form: any) {
		this._globalService.showLoaderSpinner(true);
		this.website_id_new = 1;
		var form_data = new FormData();
		form_data.append("import_file", this.xls_file);
		form_data.append('website_id', this.website_id_new);
		console.log(form_data);
		this._hsnCodeService.hsncodeImportInsert(form_data).subscribe(
			data => {
				this.dialogRef.close();
			},
			err => console.log(err),
			function () {
				//completed callback
				this._globalService.showLoaderSpinner(false);
			}
		);
	}

	closeDialog() {
		this.dialogRef.close();
	}
}



