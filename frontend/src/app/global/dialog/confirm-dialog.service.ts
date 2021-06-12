import { Observable } from 'rxjs';
import { ConfirmDialog,AlertDialog } from './confirm-dialog.component';
import { MatDialogRef, MatDialog, MatDialogConfig } from '@angular/material';
import { Injectable } from '@angular/core';


@Injectable()
export class DialogsService {

    constructor(private dialog: MatDialog) {}

    public confirm(title: string, message: string, okBtn: string =null, cancelBtn: string =null, disableClose: boolean = false): Observable<boolean> {

        let dialogRef: MatDialogRef<ConfirmDialog>;
        
        dialogRef = this.dialog.open(ConfirmDialog,{ disableClose: disableClose});
        dialogRef.componentInstance.title = title;
        dialogRef.componentInstance.message = message;
        dialogRef.componentInstance.okBtn = (okBtn)?okBtn:'OK';
        dialogRef.componentInstance.cancelBtn = (cancelBtn)?cancelBtn:'Cancel';

        return dialogRef.afterClosed();
    }

    public alert(title: string, message: string): Observable<boolean> {

        let dialogRef: MatDialogRef<AlertDialog>;

        dialogRef = this.dialog.open(AlertDialog);
        dialogRef.componentInstance.title = title;
        dialogRef.componentInstance.message = message;

        return dialogRef.afterClosed();
    }

        
}