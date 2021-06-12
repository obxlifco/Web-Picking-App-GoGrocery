import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeliverySlotComponent } from './delivery-slot.component';

describe('DeliverySlotComponent', () => {
  let component: DeliverySlotComponent;
  let fixture: ComponentFixture<DeliverySlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeliverySlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeliverySlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
