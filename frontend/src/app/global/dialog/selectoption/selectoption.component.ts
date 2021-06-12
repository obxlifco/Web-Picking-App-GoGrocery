import { Component,OnInit,Inject, Output, EventEmitter, Input} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';


@Component({
  selector: 'app-selectoption',
  templateUrl: './selectoption.component.html',
  styleUrls: ['./selectoption.component.css']
})
export class SelectOptionComponent implements OnInit {
  
  public selectedWareHouseDatails = {};
  public selectedOptionData = {};
  constructor(
    public dialogRef: MatDialogRef<SelectOptionComponent>,
    @Inject(MAT_DIALOG_DATA) public data,
  ) { }

  ngOnInit() {

  }
  
	onChangeLocation(){
    this.selectedOptionData = {
      selectedOptionId : 1,
      selectedOptionName : 'Change Location'
    }
    this.dialogRef.close(this.selectedOptionData);
  }
  
	onChangeStoreType() {
    this.selectedOptionData = {
      selectedOptionId : 2,
      selectedOptionName : 'Change Store Type'
    }
    this.dialogRef.close(this.selectedOptionData);
  }

	onChangeWareHouse() {
    this.selectedOptionData = {
      selectedOptionId : 3,
      selectedOptionName : 'Change warehouse'
    }
    this.dialogRef.close(this.selectedOptionData);
  }

  close_dialog(){
    this.dialogRef.close();
  }

}
