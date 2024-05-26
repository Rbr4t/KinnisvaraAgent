import { useState, useEffect } from "react";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import { Box } from "@mui/material";

export default function Select({
  kohad = [],
  onAsukohtChange,
  disabled,
  clear,
}) {
  const [asukoht, setAsukoht] = useState("");
  const handleChange = (e, newValue) => {
    setAsukoht(newValue);
    onAsukohtChange(newValue);
  };

  return (
    <Autocomplete
      disabled={disabled}
      id="country-select-demo"
      options={kohad}
      onInputChange={(event, newInputValue, reason) => {
        handleChange(event, newInputValue);
      }}
      autoHighlight
      getOptionLabel={(option) => option}
      renderOption={(props, option) => (
        <Box
          component="li"
          sx={{ "& > img": { mr: 2, flexShrink: 0 } }}
          {...props}
        >
          {option}
        </Box>
      )}
      renderInput={(params) => (
        <TextField
          {...params}
          inputProps={{
            ...params.inputProps,
            autoComplete: "new-password", // disable autocomplete and autofill
          }}
        />
      )}
    />
  );
}
