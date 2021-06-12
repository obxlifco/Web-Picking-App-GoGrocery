import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SubstituteProductComponent } from './substitute_product.component';

describe('SubstituteProductComponent', () => {
  let component: SubstituteProductComponent;
  let fixture: ComponentFixture<SubstituteProductComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SubstituteProductComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SubstituteProductComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
