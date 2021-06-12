import {
    Component, OnInit, Inject, Optional
}
from '@angular/core';
import {
    MatDialogRef, MAT_DIALOG_DATA, MatDialog
}
from '@angular/material';
import {
    Router
}
from '@angular/router';
import {
    UnitService
}
from './settings.unit.service';
import {
    GlobalService
}
from '../../global/service/app.global.service';
@
Component({
    templateUrl: './templates/add_unit.html',
    providers: [UnitService]
})
export class UnitAddEditComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public ipaddress: any;
    constructor(
        private _unitService: UnitService,
        private _globalService: GlobalService,
        private _router: Router,
        private dialogRef: MatDialogRef < UnitAddEditComponent > ,
        public dialog: MatDialog, @Optional()@ Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
            let containerElem: HTMLElement = < HTMLElement > document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
        });
        this.ipaddress = _globalService.getCookie('ipaddress'); //get user ip from cookie
    }
    ngOnInit() {
        this.formModel.unitId = this.data;
        if (this.formModel.unitId > 0) {
            this._unitService.unitLoad(this.formModel.unitId).subscribe(
                data => {
                    this.response = data;
                    if (this.formModel.unitId > 0) {
                        this.formModel.unitId = this.response.api_status.id;
                        this.formModel.unitName = this.response.api_status.unit_name;
                        this.formModel.unitFullName = this.response.api_status.unit_full_name;
                        this.formModel.status = this.response.api_status.isblocked;
                    } else {
                        this.formModel.unitId = 0;
                    }
                },
                err => console.log(err),
                function() {
                    //completed callback
                }
            );
        }
    }
    addEditUnit(form: any) {
        this.errorMsg = '';
        let data: any = {};
        data.website_id = 1;
        data.company_id = 1;
        data.unit_name = this.formModel.unitName;
        data.isblocked = this.formModel.status;
        data.unit_full_name = this.formModel.unitFullName;
        if (this.ipaddress) {
            data.ip_address = this.ipaddress;
        } else {
            data.ip_address = '';
        }
        if (this.formModel.unitId < 1) {
            data.createdby = this._globalService.getUserId();
        }
        data.updatedby = this._globalService.getUserId();
        this._unitService.unitAddEdit(data, this.formModel.unitId).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                    this.closeDialog();
                } else {
                    this.errorMsg = this.response.message;
                }
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
    }
    closeDialog() {
        this.dialogRef.close();
    }
}