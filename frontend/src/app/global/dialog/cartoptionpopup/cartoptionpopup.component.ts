import { FormGroup } from '@angular/forms';
import { Component, forwardRef, Inject, OnInit, Optional } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material";
import { CartService } from "../../service/cart.service";

@Component({
  selector: "app-cartoptionpopup",
  templateUrl: "./cartoptionpopup.component.html",
  styleUrls: ["./cartoptionpopup.component.css"],
})
export class CartoptionpopupComponent implements OnInit {
  custom_field_value: any = "";
  preparationValues: [];
  fieldValue: any;
  filedShowValue: any;
  fieldLabel: string;
  isVisible: Boolean;
  constructor(
    @Inject(forwardRef(() => CartService)) private cartService: CartService,
    private dialogRef: MatDialogRef<CartoptionpopupComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) public customFields: any
  ) {}

  ngOnInit() {
    console.log(this.customFields);
    this.fieldLabel = this.customFields[0].field_name;
    this.filedShowValue = this.customFields[0].value;
    this.preparationValues = this.filedShowValue.split("#");
    this.fieldValue = this.preparationValues.filter(String);
  }
  close_dialog() {
    this.dialogRef.close()
  }
  addToCart() {
    this.dialogRef.close({selected_preparion_unit: this.custom_field_value,prepearation_lable:this.fieldLabel});
    this.cartService.addData("confirm");
  }
}
