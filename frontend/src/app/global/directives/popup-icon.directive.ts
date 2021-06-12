import { Component,Inject, OnInit } from '@angular/core';
import {DOCUMENT} from '@angular/platform-browser';
import { MatDialogRef,MatDialog,MAT_DIALOG_DATA } from '@angular/material';
import { GlobalService } from '../service/app.global.service';

import {Global,GlobalVariable} from '.././service/global';


@Component({
  selector: 'icon-lib-dialog',
  templateUrl: 'icon-lib-dialog.html',
  providers: [Global]
})
export class PopupIconDirective implements OnInit {
    
    public icons: any = [];
    public selected_icon: string;
    constructor(
                public _global: Global,
                public _globalService: GlobalService,
                public dialogRef: MatDialogRef<PopupIconDirective> ,
                public dialog: MatDialog,
                @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
        this.selected_icon = this.data['selected_icon'];
    } 

    ngOnInit(){
        this.icons=[];
        let that = this;

        this._global.getFontAwsomes().subscribe(
            data => {
     
                this.icons =  data.icons;
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function(){
             //completed callback
            }
        );
    }

    selectIcon(icon: string){

        this.icons.forEach(item =>{
            if(item==icon){
                this.selected_icon = item;
            }
        });    
        
    }
    saveSelectedIcon(){

        this.dialogRef.close(this.selected_icon);
    }   

    closeDialog(){
        this.dialogRef.close(this.selected_icon);
    }         
}