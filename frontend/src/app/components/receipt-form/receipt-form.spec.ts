import { TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { ReceiptFormComponent } from './receipt-form';

describe('ReceiptFormComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReceiptFormComponent, ReactiveFormsModule],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
  });

  it('should create', () => {
    const fixture = TestBed.createComponent(ReceiptFormComponent);
    const component = fixture.componentInstance;
    expect(component).toBeTruthy();
  });

  it('form should be invalid when empty', () => {
    const fixture = TestBed.createComponent(ReceiptFormComponent);
    const component = fixture.componentInstance;
    expect(component.receiptForm.valid).toBeFalsy();
  });
});
