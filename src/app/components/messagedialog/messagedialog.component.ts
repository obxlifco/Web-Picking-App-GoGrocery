import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-messagedialog',
  templateUrl: './messagedialog.component.html',
  styleUrls: ['./messagedialog.component.scss']
})
export class MessagedialogComponent implements OnInit {

  price:any=1
  incomingmodaldata:any=[]
  constructor(public globalitem:GlobalitemService, 
    public dialogRef: MatDialogRef<MessagedialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { 
      // console.log("Incoming Data : ",data);
      this.incomingmodaldata=data
      this.price=this.incomingmodaldata.data.price
    }

  ngOnInit(): void {
  }

  close(){
    this.dialogRef.close()
  }
  updatePrice(){
    // console.log("price");
    // if stock = 0 then it will out of stock other wise it will be in stock
    if( this.incomingmodaldata.data.IsInstock > 0){
      if(this.price > 0){
        this.dialogRef.close({ price:this.price, data: this.incomingmodaldata});
      }else{
        this.globalitem.showError("Price must be greater than 0","Price !")
      }
    }else{
      this.dialogRef.close({ price:this.price, data: this.incomingmodaldata});
    }
    
  }

}
