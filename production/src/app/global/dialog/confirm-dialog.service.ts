import { Observable } from 'rxjs';
import { ConfirmDialog,AlertDialog } from './confirm-dialog.component';
import { MatDialogRef, MatDialog, MatDialogConfig } from '@angular/material';
import { Injectable } from '@angular/core';
@Injectable()
export class DialogsService {
    constructor(
        private dialog: MatDialog
    ) {

    }
    public confirm(title: string, message: string): Observable<boolean> {
        let dialogRef: MatDialogRef<ConfirmDialog>;
        dialogRef = this.dialog.open(ConfirmDialog);
        dialogRef.componentInstance.title = title;
        dialogRef.componentInstance.message = message;
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