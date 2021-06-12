import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeliveryoptionsComponent } from './deliveryoptions.component';

describe('DeliveryoptionsComponent', () => {
  let component: DeliveryoptionsComponent;
  let fixture: ComponentFixture<DeliveryoptionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeliveryoptionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeliveryoptionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
