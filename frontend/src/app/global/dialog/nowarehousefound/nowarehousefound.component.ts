import { Component,OnInit,Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-nowarehousefound',
  templateUrl: './nowarehousefound.component.html',
  styleUrls: ['./nowarehousefound.component.css']
})
export class NowarehousefoundComponent implements OnInit {

  constructor(public dialogRef: MatDialogRef<NowarehousefoundComponent>,
    @Inject(MAT_DIALOG_DATA) public data,) { }

  ngOnInit() {

  }
  goBack() {
  	this.dialogRef.close();

  }

}
