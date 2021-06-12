import { Component, OnInit,Output,EventEmitter, Inject, PLATFORM_ID} from '@angular/core';
import {CheckoutService} from '../../../../global/service/checkout.service';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-deliveryoptions',
  templateUrl: './deliveryoptions.component.html',
  styleUrls: ['./deliveryoptions.component.css']
})
export class DeliveryoptionsComponent implements OnInit {

  public allDeliverySlot = [];
  public selectedDeliverySlot;
  public tomeSlot:any;
  public delivery_note:any;
  @Output() changeTimeSlot = new EventEmitter();
  @Output() custom_msg = new EventEmitter();
  @Output() messageToEmit = new EventEmitter<string>();

  constructor(private _checkout:CheckoutService,    @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {

    this.getDeliverySlot();
    }
  }
  /**
   * Method to get all delivery address
   * @access public
  */
  getDeliverySlot() {
    this._checkout.getAllDeliverySlot().subscribe(response => {
      console.log("********************** Delivery time slot options ***************");
      console.log(response);

      if(response && response['status'] == 1) {
        response['delivery_slot'].forEach(slotData => {
          if(slotData && slotData['available_slot'] && slotData['available_slot'].length > 0) {
            slotData['available_slot'].forEach(availableSlotData => {
              if(availableSlotData['is_active'] == 'Yes') {
                let slotName = availableSlotData['based_on'] == 'SameDay' ? 'Same Day' : 'Next Day';
                availableSlotData['slot_name'] = slotName;
                availableSlotData['delivery_date'] = slotData['delivery_date'];
                this.allDeliverySlot.push(availableSlotData);
                this.tomeSlot = this.allDeliverySlot[0];
                this.onChangeTimeSlot(this.tomeSlot);
              }
            })
          }
        })
      }
      console.log("****************** All delivery slot ****************");
      console.log(this.allDeliverySlot);
 
    });

  }
  /**
   * Method on chnaging time slot
   * @access public
  */
  onChangeTimeSlot(slotId) {
    this.changeTimeSlot.emit(slotId);
  }

  get_special_instruction() {
    console.log("delivery option page")
    console.log(this.delivery_note);
    this.custom_msg.emit(this.delivery_note);
  }

  sendMessageToParent(message: string) {
    this.messageToEmit.emit(this.delivery_note)
  }
}
