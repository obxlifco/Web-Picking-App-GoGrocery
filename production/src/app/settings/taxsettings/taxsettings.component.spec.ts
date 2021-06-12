import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxsettingsComponent } from './taxsettings.component';

describe('TaxsettingsComponent', () => {
  let component: TaxsettingsComponent;
  let fixture: ComponentFixture<TaxsettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxsettingsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxsettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
