import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ModalService } from 'src/app/services/modal/modal.service';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-assaignpicker',
  templateUrl: './assaignpicker.component.html',
  styleUrls: ['./assaignpicker.component.scss']
})
export class AssaignpickerComponent implements OnInit {

  pickername:any='';
  modaldata:any=[]
  constructor(public modalservice : ModalService,
    public globalitem:GlobalitemService,
    public apiservice : ApiService,
    public dialogRef: MatDialogRef<AssaignpickerComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
    ) {
      // console.log("incoming modal data : ",data);
      
      
      this.modaldata=data
      // this.pickername=this.modaldata.data.billnumber
     }

  ngOnInit(): void {
  }

  closeModal(){
    this.dialogRef.close();    
  }
  savePickerName(){
    
    if(this.pickername.length !== 0){

      let data = {
        website_id: this.modaldata.data.website_id,
        user_id: this.modaldata.data.user_id,
        picker_name: this.pickername,
        order_id: this.modaldata.data.order_id,
        shipment_id: this.modaldata.data.shipment_id,
        order_status: this.modaldata.data.order_status
      }
      

    this.apiservice.postData('picker-generatepicklist/', data).subscribe((data: any) => 
    {
      if(data.status === 1){
        this.globalitem.showSuccess(data.message,"Name Updated")
        this.dialogRef.close({ event: 'close', pickername: this.pickername});
      }else{
        this.globalitem.showError(data.message,"")
        // this.dialogRef.close({ event: 'close', billnumber: this.bill_number});
      }
      
    })
  }else{
    this.globalitem.showError("First you need to Enter Picker name","Bill Number")
  }
  }
}
