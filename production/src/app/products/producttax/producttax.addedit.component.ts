import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';


@Component({
    selector: 'app-producttax.addedit',
    templateUrl: 'templates/producttax.addedit.html',
    providers: [Global]
})

export class ProducttaxAddeditComponent implements OnInit {
    public ipaddress: any;
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;

    constructor(
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        private dialogRef: MatDialogRef<ProducttaxAddeditComponent>,
        public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
            let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
         });
         this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {

        this.formModel.formId =this.data; 
        if (this.formModel.formId > 0) {
            this.global.getWebServiceData('view_producttaxclass','GET','',this.formModel.formId).subscribe(Response => {
                console.log(Response)
                let data=Response.api_status;
                this.formModel.name = data.name;
            }, err => {
                console.log(err)
            })
        } 
    }

    addEdit(form: any) {
        setTimeout(() => {
            this._globalService.showLoaderSpinner(false);
        });
        let data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.name = this.formModel.name;
        if (this.formModel.formId > 0) {
            data.id = this.formModel.formId;
        }
        data={"value":data};
        console.log(data)
        this.global.getWebServiceData('producttaxclass','POST',data,'').subscribe(res => { 
            if (res['status'] == '1') { // success response 
                this.closeDialog();
                this._globalService.showToast(res['message']);
                this._router.navigate(['/product_tax_class/']);
            } else {
                this._globalService.showToast(res['message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
        }, err => {

        })
    }
    closeDialog(){
        this.dialogRef.close();
    } 
}