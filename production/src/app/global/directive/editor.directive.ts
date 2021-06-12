import { Component,Inject } from '@angular/core';
import { DOCUMENT } from '@angular/platform-browser';
import { MatDialogRef, MatDialog, MAT_DIALOG_DATA } from '@angular/material';
@Component({
  selector: 'dialog-editor',
  template: `
  	<div class="loada" *ngIf="showLoader">
        <mat-spinner strokeWidth="5"></mat-spinner>
    </div>
    <ckeditor [config]="config" #editor name="editor" [(ngModel)]="content" debounce="500"></ckeditor>
  	<mat-dialog-actions layout="row" *ngIf="!showLoader">
		  	<span flex></span>
		  	<button mat-raised-button class="btn-main" type="button" (click)="saveEditor(editor.value)">Save</button>
		  	<button mat-raised-button class="btn-line" type="button" (click)="closeDialog()">Cancel</button>
	</mat-dialog-actions>
  `,
})
export class EditorDialog {
    public showLoader: boolean = true;
    public content: string;
    public config: any;
    constructor(
                public dialogRef: MatDialogRef<EditorDialog> ,
                public dialog: MatDialog,
                @Inject(MAT_DIALOG_DATA) public data: any
                ) {
    				this.content = data.value;
                    this.config = {uiColor: '#ffffff',
                        toolbar: [
                                    { name: 'tools', items: ['Maximize'] },
                                    { name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
                                    { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
                                    { name: 'links', groups: [ 'Link', 'Unlink', 'Anchor'] },
                                    { name: 'document', items: ['Source']},  
                                    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'CopyFormatting', 'RemoveFormat' ] },
                                    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
                                    { name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize' ] },
                                    { name: 'colors', items: [ 'TextColor', 'BGColor' ] },
                                  ]         
                    };
                    setTimeout(()=>{
                        this.showLoader = !this.showLoader;
                    }, 1000);

                    dialog.afterOpen.subscribe(() => {
                       let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
                       containerElem.classList.remove('pop-box-up');
                    }); 
    			} 

    closeDialog() {
    	this.dialogRef.close();
    }

    saveEditor(val){
    	let data = this.data;
    	data.value = val;
    	this.dialogRef.close(data);
    }            
}