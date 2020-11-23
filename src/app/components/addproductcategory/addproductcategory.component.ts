import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-addproductcategory',
  templateUrl: './addproductcategory.component.html',
  styleUrls: ['./addproductcategory.component.scss']
})
export class AddproductcategoryComponent implements OnInit {

  name:any;
  category:any;
  constructor(public dialogRef: MatDialogRef<AddproductcategoryComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
      console.log("modal incoming data : ",data);
     }

  ngOnInit(): void {
  }

  listItem(name:any,category:any){
    console.log(name , category);
    
    this.name=name
    this.category=category
    let data={
      name:this.name,
      category:this.category
    }
    this.dialogRef.close({ event: 'close', data: data});
  }
  closeModal():void{
    this.dialogRef.close();
  }

}
