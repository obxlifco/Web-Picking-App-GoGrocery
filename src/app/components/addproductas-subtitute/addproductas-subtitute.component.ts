import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-addproductas-subtitute',
  templateUrl: './addproductas-subtitute.component.html',
  styleUrls: ['./addproductas-subtitute.component.scss']
})
export class AddproductasSubtituteComponent implements OnInit {

  modalData:any=[]
  constructor(
    public apiService: ApiService,
    public globalitem: GlobalitemService,
    public dialogRef: MatDialogRef<AddproductasSubtituteComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) { 
    console.log("incoming data modal : ",data);
    
  this.modalData=data

  }

  ngOnInit(): void {
  }
  addproduct(){
    let data={
      product_id:this.modalData.data.product_id,
      related_product_id:this.modalData.data.related_product_id,
      // related_product_type:this.modalData.data.related_product_type
      related_product_type:5
    }
    this.apiService.postData(this.modalData.data.URl, data).subscribe((data: any[]) => {
      console.log(data);
      this.dialogRef.close({ event: 'close', data: "none"});

    })
  } 
  
  closeModal(){
    this.dialogRef.close()
  }


}
