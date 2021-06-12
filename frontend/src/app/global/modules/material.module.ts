import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatTableModule} from '@angular/material/table';
import {MatSliderModule} from '@angular/material/slider';
// Importing all material module and export all module to use on another feature module
import { FormsModule } from '@angular/forms';
import {
	    MatExpansionModule,
	    MatMenuModule,
	    MatSlideToggleModule,
	    MatIconModule,
	    MatButtonToggleModule,
	    MatButtonModule,
	    MatCheckboxModule,
	    MatInputModule,
	    MatTooltipModule,
	    MatTabsModule,
	    MatSelectModule,
	    MatDialogModule,
	    MatRadioModule,
	    MatSnackBarModule,
	    MatProgressSpinnerModule,
	    MatProgressBarModule,
	    MatChipsModule,
	    MatAutocompleteModule} from '@angular/material'; 
@NgModule({
	declarations : [

	],
	imports : [
		MatExpansionModule,
		MatMenuModule,
	    MatSlideToggleModule,
	    MatIconModule,
	    MatButtonToggleModule,
	    MatButtonModule,
	    MatCheckboxModule,
	    MatInputModule,
	    MatTooltipModule,
	    MatTabsModule,
	    MatSelectModule,
	    MatDialogModule,
	    MatRadioModule,
	    MatSnackBarModule,
	    MatProgressSpinnerModule,
	    MatProgressBarModule,
	    MatChipsModule,
		MatAutocompleteModule,
		FormsModule,
		MatTableModule
	],
	exports : [
		MatExpansionModule,
		MatMenuModule,
	    MatSlideToggleModule,
	    MatIconModule,
	    MatButtonToggleModule,
	    MatButtonModule,
	    MatCheckboxModule,
	    MatInputModule,
	    MatTooltipModule,
	    MatTabsModule,
	    MatSelectModule,
	    MatDialogModule,
	    MatRadioModule,
	    MatSnackBarModule,
	    MatProgressSpinnerModule,
	    MatProgressBarModule,
	    MatChipsModule,
		MatAutocompleteModule,
		FormsModule,
		MatTableModule
	]
})
export class MaterialModule {}