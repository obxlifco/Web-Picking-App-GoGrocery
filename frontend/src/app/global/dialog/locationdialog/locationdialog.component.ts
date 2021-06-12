import { Component, OnInit,Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
@Component({
  selector: 'app-locationdialog',
  templateUrl: './locationdialog.component.html',
  styleUrls: ['./locationdialog.component.css']
})
export class LocationdialogComponent implements OnInit {
	constructor(
		public dialogRef: MatDialogRef<LocationdialogComponent>,
		@Inject(MAT_DIALOG_DATA) public data,
		public dialog: MatDialog
	) { }

  ngOnInit() {

  }
  enableLocation() {
  	  console.log("************** Enable location clicked ****************");
		let currentPosition = {
		  'latitude' : 25.2048,
		  'longitude' : 55.2708
		};
		if(navigator.geolocation) {
			navigator.geolocation.getCurrentPosition((position) => {
			// console.log('position details');
			// console.log(position);
			if(position && position['coords']) {
			  	// console.log('positio enter');
				  currentPosition['latitude'] = position['coords']['latitude'];
					currentPosition['longitude'] = position['coords']['longitude'];
					currentPosition['accuracy'] = position['coords']['accuracy'];
				}
				this.dialogRef.close(currentPosition);
				//this.closeDialog(currentPosition);
			},
		  (error) => {
			 this.dialogRef.close(currentPosition);
		  }
		  );
			//console.log("****************** Position data ***************",positionData);
		} else {
		  this.dialogRef.close(currentPosition);
		}
		//this.dialogRef.close();
	}
}