import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddnewdeliveryaddressComponent } from './addnewdeliveryaddress.component';

describe('AddnewdeliveryaddressComponent', () => {
  let component: AddnewdeliveryaddressComponent;
  let fixture: ComponentFixture<AddnewdeliveryaddressComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddnewdeliveryaddressComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddnewdeliveryaddressComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
