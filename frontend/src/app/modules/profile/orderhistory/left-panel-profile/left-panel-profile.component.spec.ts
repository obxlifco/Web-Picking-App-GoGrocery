import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LeftPanelProfileComponent } from './left-panel-profile.component';

describe('LeftPanelProfileComponent', () => {
  let component: LeftPanelProfileComponent;
  let fixture: ComponentFixture<LeftPanelProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LeftPanelProfileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LeftPanelProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
