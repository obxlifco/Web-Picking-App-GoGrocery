import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductimportComponent } from './productimport.component';

describe('ProductimportComponent', () => {
  let component: ProductimportComponent;
  let fixture: ComponentFixture<ProductimportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProductimportComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductimportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
