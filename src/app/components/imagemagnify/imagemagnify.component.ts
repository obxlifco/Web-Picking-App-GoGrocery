import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-imagemagnify',
  templateUrl: './imagemagnify.component.html',
  styleUrls: ['./imagemagnify.component.scss']
})
export class ImagemagnifyComponent implements OnInit {
  imagedata:any;
  constructor(public dialog: MatDialog,
    public dialogRef: MatDialogRef<ImagemagnifyComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { 
      console.log("data is : ",data);
      this.imagedata=data   
    }

  ngOnInit(): void {
  }
  closeModal(){
    this.dialogRef.close()
  }

}
