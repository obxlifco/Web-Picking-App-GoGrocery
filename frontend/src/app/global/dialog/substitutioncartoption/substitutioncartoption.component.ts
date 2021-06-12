import { SubstituteProductComponent } from './../../../modules/substitute_product/substitute_product.component';
import { Component, forwardRef, Inject, OnInit, Optional } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material";

@Component({
  selector: 'app-substitutioncartoption',
  templateUrl: './substitutioncartoption.component.html',
  styleUrls: ['./substitutioncartoption.component.css']
})
export class SubstitutioncartoptionComponent implements OnInit {
  custom_field_value: any = "";
  preparationValues: [];
  fieldValue: any;
  filedShowValue: any;
  fieldLabel: string;
  isVisible: Boolean;
  constructor(
    private dialogRef: MatDialogRef<SubstitutioncartoptionComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) public custom_fields: any,
    // private SubstituteProductComponent:SubstituteProductComponent
  ) { }

  ngOnInit() {
    console.log(this.custom_fields);
    this.fieldLabel = this.custom_fields[0].field_name;
    this.filedShowValue = this.custom_fields[0].value;
    this.preparationValues = this.filedShowValue.split("#");
    this.fieldValue = this.preparationValues.filter(String);
  }
  close_dialog() {
    this.dialogRef.close()
  }
  addItem() {
    this.dialogRef.close({custom_field_value:this.custom_field_value,fieldlabel:this.fieldLabel});
  }

}
