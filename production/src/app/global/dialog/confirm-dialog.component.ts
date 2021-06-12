import { MatDialogRef,MatDialog } from '@angular/material';
import { Component } from '@angular/core';

@Component({
    selector: 'confirm-dialog',
    template: `
        <h3><p>{{ title }}</p></h3>
        <p>{{ message }}</p>
        <button type="button" mat-raised-button class="btn-line"
            (click)="dialogRef.close(false)">Cancel</button>
        <button type="button" mat-raised-button class="btn-main" 
            (click)="dialogRef.close(true)">OK</button>
        
    `,
})
export class ConfirmDialog {

    public title: string;
    public message: string;

    constructor(public dialogRef: MatDialogRef<ConfirmDialog>,public dialog: MatDialog) {
       dialog.afterOpen.subscribe(() => {
               let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
               containerElem.classList.remove('pop-box-up');
            }); 
    }
}

@Component({
    selector: 'alert-dialog',
    template: `
        <h3><p>{{ title }}</p></h3>
        <p>{{ message }}</p>
        <button type="button" mat-raised-button class="btn-main"
            (click)="dialogRef.close(false)">OK</button>
    `,
})
export class AlertDialog {

    public title: string;
    public message: string;

    constructor(public dialogRef: MatDialogRef<AlertDialog>,public dialog: MatDialog) {
         dialog.afterOpen.subscribe(() => {
               let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
               containerElem.classList.remove('pop-box-up');
            });
    }
}