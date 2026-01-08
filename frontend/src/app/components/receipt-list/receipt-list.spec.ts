import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { ReceiptListComponent } from './receipt-list'; // Fix: Use correct class name

describe('ReceiptListComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReceiptListComponent],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
  });

  it('should create', () => {
    const fixture = TestBed.createComponent(ReceiptListComponent);
    const component = fixture.componentInstance;
    expect(component).toBeTruthy();
  });
});
