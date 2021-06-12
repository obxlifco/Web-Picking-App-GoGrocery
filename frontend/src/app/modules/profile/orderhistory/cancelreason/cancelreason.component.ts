import { Component, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-cancelreason',
  templateUrl: './cancelreason.component.html',
  styleUrls: ['./cancelreason.component.css']
})
export class CancelreasonComponent implements OnInit {
  public return_note_arr_full = [
    {id: 1, text: 'Wrong Product Selected'},
    {id: 2, text: 'Wrong Price'},
    {id: 3, text: 'Ordered By Mistake'},
    {id: 4, text: 'Others'}
  ];
	public formModel: any = {};
  constructor(
    public dialogRef: MatDialogRef<CancelreasonComponent>,

  ) { }

  ngOnInit() {
  }
  addEdit(data:any){
    let postdata=data.value;
    this.dialogRef.close(postdata);
  }
  cancel_btn(){
    this.dialogRef.close();
  }
}
