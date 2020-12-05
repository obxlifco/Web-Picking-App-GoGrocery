import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-messagedialog',
  templateUrl: './messagedialog.component.html',
  styleUrls: ['./messagedialog.component.scss']
})
export class MessagedialogComponent implements OnInit {

  price:any
  incomingmodaldata:any=[]
  constructor( public dialogRef: MatDialogRef<MessagedialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { 
      console.log("Incoming Data : ",data);
      this.incomingmodaldata=data
    }

  ngOnInit(): void {
  }

  close(){
    this.dialogRef.close()
  }
  updatePrice(){
    this.dialogRef.close({ price:this.price, data: this.incomingmodaldata});
  }

}
