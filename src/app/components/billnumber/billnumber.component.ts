import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ModalService } from 'src/app/services/modal/modal.service';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-billnumber',
  templateUrl: './billnumber.component.html',
  styleUrls: ['./billnumber.component.scss']
})
export class BillnumberComponent implements OnInit {

  bill_number:any='';
  modaldata:any=[]
  constructor(public modalservice : ModalService,
    public globalitem:GlobalitemService,
    public apiservice : ApiService,
    public dialogRef: MatDialogRef<BillnumberComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
    ) {
      this.modaldata=data
     }

  ngOnInit(): void {
  }

  closeModal(){
    let billdta:any
    if(this.modaldata.data.billnumber === "Enter Bill Number"){
      billdta="Enter Bill Number"
      this.dialogRef.close({ event: 'close', billnumber:billdta})
    }else{
      billdta=this.modaldata.data.billnumber
      this.dialogRef.close({ event: 'close', billnumber:billdta})
    }
    
  }
  saveBillNumber(){
    
    let data={
      website_id:this.modaldata.data.website_id,
      order_id:this.modaldata.data.order_id,
      user_id:this.modaldata.data.user_id,
      order_bill_number:this.bill_number
    }
    if(this.bill_number.length !== 0){
    this.apiservice.postData('picker-updateorderbillnumber/', data).subscribe((data: any) => 
    {
      if(data.status === 1){
        this.globalitem.showSuccess("Bill numbe updated successfully ","Bill Updated")
        this.dialogRef.close({ event: 'close', billnumber: this.bill_number});
      }else{
        this.globalitem.showError(data.message,"")
        // this.dialogRef.close({ event: 'close', billnumber: this.bill_number});
      }
      
    })
  }else{
    this.globalitem.showError("First you need to Enter Bill Number","Bill Number")
  }
  }

}
