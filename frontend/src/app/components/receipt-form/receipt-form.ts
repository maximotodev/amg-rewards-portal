import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ReceiptService } from '../../services/receipt';

@Component({
  selector: 'amg-receipt-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './receipt-form.html',
  styleUrl: './receipt-form.scss',
})
export class ReceiptFormComponent {
  private fb = inject(FormBuilder);
  private receiptService = inject(ReceiptService);

  // Signals for modern Angular state management
  isSubmitting = signal(false);

  // Property to hold the binary file from the 'Snap' action
  selectedFile: File | null = null;

  receiptForm = this.fb.group({
    user_id: ['AMG_USER_01'],
    merchant_name: ['', [Validators.required, Validators.minLength(2)]],
    total_amount: [null, [Validators.required, Validators.min(0.01)]],
    purchase_date: [new Date().toISOString().split('T')[0], Validators.required],
  });

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      console.log("File ready for 'Snap' logic:", file.name);
    }
  }

  onSubmit() {
    // We only proceed if the form is valid AND a file was selected
    if (this.receiptForm.valid && this.selectedFile) {
      this.isSubmitting.set(true);

      // We now pass both the JSON metadata and the binary File
      this.receiptService
        .submitReceipt(this.receiptForm.value as any, this.selectedFile)
        .subscribe({
          next: (res) => {
            alert(`Success! You earned ${res.points_earned} points.`);

            // Reset form and file state
            this.receiptForm.patchValue({ merchant_name: '', total_amount: null });
            this.selectedFile = null;
            this.isSubmitting.set(false);

            // Note: In a real app, you'd use a ViewChild to clear the HTML file input element
          },
          error: (err) => {
            console.error('API Error:', err);
            this.isSubmitting.set(false);

            // Senior Touch: Handle specific error codes
            if (err.status === 409) {
              alert('Fraud Alert: This receipt has already been submitted and processed.');
            } else if (err.status === 413) {
              alert('File too large. Please snap a smaller photo.');
            } else {
              alert('Submission failed. Please check your connection.');
            }
          },
        });
    } else if (!this.selectedFile) {
      alert('Please snap a photo of the receipt before submitting.');
    }
  }
}
