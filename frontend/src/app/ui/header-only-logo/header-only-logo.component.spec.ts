import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HeaderOnlyLogoComponent } from './header-only-logo.component';

describe('HeaderOnlyLogoComponent', () => {
  let component: HeaderOnlyLogoComponent;
  let fixture: ComponentFixture<HeaderOnlyLogoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HeaderOnlyLogoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HeaderOnlyLogoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
