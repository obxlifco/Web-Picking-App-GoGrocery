import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-editproductweight',
  templateUrl: './editproductweight.component.html',
  styleUrls: ['./editproductweight.component.scss']
})
export class EditproductweightComponent implements OnInit {

  editweightData:any=[]
  newprice:any
  newWeight:any
  notes:any
  constructor(public dialogRef: MatDialogRef<EditproductweightComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { 
      let tempdata:any=[]
      tempdata=data
      this.editweightData["data"]=tempdata.data
      console.log("edit weight data : ", this.editweightData["data"]);
      
    }

  ngOnInit(): void {
    // this.editweightData['data']=[]
  }
  // products?.quantity,products?.product.weight,products?.product.uom.uom_full_name,products?.product_price,products?.product.name,products?.productean
  closeModal(){
this.dialogRef.close()
  }

  Apply(){
    let data = {
      newprice: this.newprice,
      newweight: this.newWeight,
      notes:this.notes
    }
    this.dialogRef.close({ event: 'close', data: data });
  }
  totalweightPrice(totalweight :any,unitweight:any,unitprice:any,event:any){
    this.newprice = event.target.value/unitweight * unitprice
    console.log("price : ",event.target.value/unitweight * unitprice);
    console.log("unitweight : ",unitweight);
    console.log("unit price : ",unitprice);
    console.log("total weight : ",event.target.value);    
  }
}
