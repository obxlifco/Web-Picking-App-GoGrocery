import { MatDialogRef,MatDialog } from '@angular/material';
import { Component } from '@angular/core';
import { CookieService } from 'ngx-cookie';
@Component({
    selector: 'confirm-dialog',
    template: 
    `<section>
        <div class="pop_upbg">
            <div class="popup_wrap">
                <div class="selectstore">
                    <div class="head" style="color: red">{{ title }}</div>
                    <div class="head">{{ message }}</div>
                    <button type="button" class="add_tocard" style="width: 22%; background-color: red"
                        (click)="dialogRef.close(false)">{{cancelBtn}}</button>
                    <button type="button" class="add_tocard" style="width: 22%; float: right;" 
                        (click)="dialogRef.close(true)">{{okBtn}}</button>
                </div>
            </div>
        </div>
    </section>`,
})
export class ConfirmDialog {
    public title: string;
    public message: string;
    public okBtn: string;
    public cancelBtn: string;
    constructor( 
        public dialogRef: MatDialogRef<ConfirmDialog>,
        private _cookieService: CookieService,
        public dialog: MatDialog
    ) {

        let globalData = this._cookieService.getObject('globalData');
        dialog.afterOpen.subscribe(() => {
            let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
           
            if(globalData['lang_code'] && globalData['lang_code'] == 'th'){
                    containerElem.classList.add('thai-body');
            } else {
                containerElem.classList.remove('thai-body');
            }
        }); 
    }
}

@Component({
    selector: 'alert-dialog',
    template: `<h3><p>{{ title }}</p></h3>
        <p>{{ message }}</p>
        <button type="button" mat-raised-button class="btn-green"
            (click)="dialogRef.close(false)">OK</button>`,
})
export class AlertDialog {
    public title: string;
    public message: string;
    constructor(
        public dialogRef: MatDialogRef<AlertDialog>,
        private _cookieService: CookieService,
        public dialog: MatDialog
    ) {
        let globalData = this._cookieService.getObject('globalData');
        dialog.afterOpen.subscribe(() => {
            let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
            if(globalData['lang_code'] && globalData['lang_code'] == 'th'){
                    containerElem.classList.add('thai-body');
            } else {
                containerElem.classList.remove('thai-body');
            }
        });
    }
}